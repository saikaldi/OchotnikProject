from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegisterUserSerializer, ConfirmEmailSerializer, LoginUserSerializer
from .models import User, EmailVerification
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate
import jwt

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user = User.objects.create_user(
            email=user['email'],
            username=user['username'],
            user_status=user['user_status'],
            last_name=user['last_name']
        )
        
        # Верификациялоо кодун түзүү
        verification_code = EmailVerification.objects.create(
            user=user,
            code=EmailVerification.generate_code()
        )
        
        send_mail(
            subject='Подтверждение по email',
            message=f'Подтверждение по email для аккаунта {user.email}. Код: {verification_code.code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return Response({'message': 'Код подтверждения отправлен на ваш email'}, status=status.HTTP_201_CREATED)
    
class ConfirmRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            confirmation = EmailVerification.objects.get(user=user, code=code)
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            return Response({'message': 'Неверный код или email'}, status=status.HTTP_400_BAD_REQUEST)

        if confirmation.is_used:
            return Response({'message': 'Этот код уже был использован'}, status=status.HTTP_400_BAD_REQUEST)

        if confirmation.is_expired():
            if not confirmation.is_used:
                user.delete()
                return Response({'message': 'Код подтверждения истек, запросите код повторно'}, status=status.HTTP_400_BAD_REQUEST)

        confirmation.is_used = True
        confirmation.save()

        user.is_active = True
        user.save()

        if user.user_status != 'Студент':
            user.is_approved_by_admin = False
            user.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'message': 'Пользователь успешно подтвержден', 'token': token}, status=status.HTTP_201_CREATED)    
    
class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    
class PasswordResetView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ConfirmEmailSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        code = EmailVerification.generate_code()
        user.email_verification.code = code
        user.email_verification.save()
        send_mail(
            subject='Ссылка для сброса пароля',
            message=f'Ссылка для сброса пароля для аккаунта {user.email}: http://127.0.0.1:8000/password-reset/?code={code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=201)
    
    def get(self, request, *args, **kwargs):
        code = self.kwargs['code']  