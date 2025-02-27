from rest_framework import serializers
from .models import User
from .models import EmailVerification
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


User = get_user_model()

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    frist_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)
    user_status = serializers.ChoiceField(choices=User.STATUS_CHOICES)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Пользователь с таким именом уже существует!")
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_status=validated_data['user_status'],
            frist_name=validated_data['frist_name'],
            last_name=validated_data['last_name'],
            is_active=True
        )
        return user

    
class ConfirmRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        if not EmailVerification.objects.filter(user=data['email'], code=data['code']).exists():
            raise serializers.ValidationError("Код подтверждения не совпадает с указанным")
        if EmailVerification.objects.filter(user=data['email'], is_used=True).exists():
            raise serializers.ValidationError("Код подтверждения уже использован")
        return data
    
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Аккаунт не активирован')
                data['user'] = user
            else:
                raise serializers.ValidationError('Неверный email или пароль')
        else:
            raise serializers.ValidationError('Email и пароль обязательны')
        return data

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь с таким email не найден.')
        return value

class ConfirmPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь с таким email не найден.')
        return value
    
    