from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
import uuid
from drf_spectacular.utils import extend_schema
from .serializers import UserRegistrationSerializer, LoginSerializer, PasswordResetSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
        description="Регистрация нового пользователя."
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Пользователь зарегистрирован успешно",
                "user": UserRegistrationSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={200: 'Токен доступа и обновления'},
        description="Авторизация пользователя."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return Response(
                {"error": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    @extend_schema(
        request=PasswordResetSerializer,
        responses={200: 'Сообщение для сброса пароля отправлено на указанный email'},
        description="Сброс пароля по электронной почте."
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                reset_token = str(uuid.uuid4())

                reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
                send_mail(
                    'Запрос сброса пароля',
                    f'Нажмите на следующую ссылку, чтобы сбросить пароль: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Сообщение отправлено."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    "error": "Пользователь с таким электронным адресом не существует"
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
