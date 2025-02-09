from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, LoginUserSerializer, RequestPasswordResetSerializer, ConfirmPasswordResetSerializer
from .models import User, EmailVerification
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import secrets
import string

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    @extend_schema(
        summary="Регистрация нового пользователя",
        description="Регистрация нового пользователя",
        request=RegisterUserSerializer,
        responses={
            201: {
                'description': 'Код подтверждения отправлен на email',
                'content': {
                    'application/json': {
                        'example': {'message': 'Код подтверждения отправлен'}
                    }
                }
            },
            500: {
                'description': 'Ошибка отправки email',
                'content': {
                    'application/json': {
                        'example': {'message': 'Ошибка отправки email'}
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                name="Пример запроса",
                value={
                    "frist_name": "Имя",
                    "last_name": "Фамилия",
                    "username": "Имя пользователя",
                    "user_status": "Пользователь",
                    "email": "user@example.com",
                    "password": "securepassword123",
                    "password_confirm": "securepassword123"
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data

        user = User.objects.create_user(
            frist_name=user_data['frist_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            user_status=user_data['user_status'],
        )

        verification_code = EmailVerification.objects.create(
            user=user,
            code=EmailVerification.generate_code()
        )

        try:
            send_mail(
                subject='Подтверждение по email',
                message=f'Код подтверждения: {verification_code.code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            user.delete()
            return Response({'message': 'Ошибка отправки email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'Код подтверждения отправлен'}, status=status.HTTP_201_CREATED)  

class ConfirmRegistrationView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="Подтверждение email пользователя",
        description="Подтверждение email пользователя",
        request=OpenApiTypes.OBJECT,
        responses={
            200: {
                'description': 'Аккаунт подтвержден',
                'content': {
                    'application/json': {
                        'example': {'message': 'Аккаунт подтвержден', 'token': 'yBE6C33a8MC4JtB4i-R2srXoLohf4uX0b_3f3PB3t8Y'}
                    }
                }
            },            
            400: {
                'description': 'Неверный email',
                'content': {
                    'application/json': {
                        'example': {'message': 'Неверный email'}
                    }
                }
            },
            500: {
                'description': 'Ошибка подтверждения регистрации',
                'content': {
                    'application/json': {
                        'example': {'message': 'Ошибка подтверждения регистрации'}
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                name="Пример запроса",
                value={
                    "email": "user@example.com",
                    "code": "242171"
                },
                request_only=True
            )
        ]
    )   
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            code = request.data.get('code')
            user = User.objects.get(email=email)
            confirmation = EmailVerification.objects.get(user=user, code=code)
            if confirmation.is_used:
                return Response({'message': 'Код уже использован'}, status=status.HTTP_400_BAD_REQUEST)
            if confirmation.is_expired():
                return self.send_new_code(user)
            confirmation.is_used = True
            confirmation.save()
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'message': 'Аккаунт подтвержден', 'token': token}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Неверный email'}, status=status.HTTP_400_BAD_REQUEST)
        except EmailVerification.DoesNotExist:
            return Response({'message': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Ошибка подтверждения регистрации'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_new_code(self, user):
        try:
            verification_code = EmailVerification.objects.create(
                user=user,
                code=EmailVerification.generate_code()
            )
            send_mail(
                subject='Подтверждение по email',
                message=f'Код подтверждения: {verification_code.code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({'error': 'Время кода истекло',
                            'message': 'Новый код подтверждения отправлен'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Ошибка отправки нового кода'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer
    @extend_schema(
        summary="Аутентификация пользователя",
        description="Аутентификация пользователя",
        request=LoginUserSerializer,
        responses={
            200: {
                'description': 'Успешная аутентификация',
                'content': {
                    'application/json': {
                        'example': {'token': 'access_token'}
                    }
                }
            },
            400: {
                'description': 'Ошибка аутентификации',
                'content': {
                    'application/json': {
                        'example': {'message': 'Аккаунт не активирован'}
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                name="Пример запроса",
                value={
                    "email": "user@example.com",
                    "password": "securepassword123"
                },
                request_only=True
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            return Response({'message': 'Аккаунт не активирован'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)    

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        summary="Запрос на сброс пароля",
        description="Запрос на сброс пароля",
        request=RequestPasswordResetSerializer,
        responses={
            200: {
                'description': 'Ссылка для смены пароля отправлена на email',
                'content': {
                    'application/json': {
                        'example': {'message': 'Ссылка для смены пароля отправлена на ваш email.'}
                    }
                }
            },
            404: {
                'description': 'Пользователь не найден',
                'content': {
                    'application/json': {
                        'example': {'message': 'Пользователь не найден'}
                    }
                }
            },
            500: {
                'description': 'Ошибка отправки email',
                'content': {
                    'application/json': {
                        'example': {'message': 'Ошибка отправки email'}
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                name="Пример запроса",
                value={
                    "email": "user@example.com"
                },
                request_only=True
            )
        ]
    )  
    def post(self, request):
        try:
            serializer = RequestPasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            # token = secrets.token_urlsafe()                                 # Определение токена
            # reset_url = f"{settings.BASE_URL}/api/v1/auth/confirm-password-reset/?token={token}"
            reset_url = f"{settings.BASE_URL}/api/v1/auth/confirm-password-reset/"
            send_mail(
                'Перейдите по ссылке, чтобы сменить пароль',
                f'Перейдите по ссылке, чтобы сменить пароль: {reset_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            return Response({'message': 'Ссылка для смены пароля отправлена на ваш email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Ошибка отправки email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConfirmPasswordResetView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Подтверждение сброса пароля и изменение пароля",
        description="Подтверждение сброса пароля",
        request=ConfirmPasswordResetSerializer,
        responses={
            200: {
                'description': 'Пароль успешно изменен',
                'content': {
                    'application/json': {
                        'example': {'message': 'Пароль успешно изменен.'}
                    }
                }
            },
            404: {
                'description': 'Пользователь не найден',
                'content': {
                    'application/json': {
                        'example': {'message': 'Пользователь не найден'}
                    }
                }
            },
            500: {
                'description': 'Ошибка изменения пароля',
                'content': {
                    'application/json': {
                        'example': {'message': 'Ошибка изменения пароля'}
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                name="Пример запроса",
                value={
                    "email": "user@example.com",
                    "new_password": "newsecurepassword123",
                    "new_password_confirm": "newsecurepassword123"
                },
                request_only=True
            )
        ]
    )
    
    def post(self, request):
        try:
            serializer = ConfirmPasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Ошибка изменения пароля'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)