from rest_framework import serializers
from .models import User
from .models import EmailVerification
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password


User = get_user_model()

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)
    user_status = serializers.ChoiceField(choices=User.STATUS_CHOICES)
    last_name = serializers.CharField(max_length=50)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_status=validated_data['user_status'],
            frist_name=validated_data['frist_name'],
            last_name=validated_data['last_name'],
            is_active=True
        )
        return user
    
class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        if not EmailVerification.objects.filter(user=data['email'], code=data['code']).exists():
            raise serializers.ValidationError("Код подтверждения не совпадает с указанным")
        if EmailVerification.objects.filter(user=data['email'], is_used=True).exists():
            raise serializers.ValidationError("Код подтверждения уже использован")
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Пользователь с таким email не существует")
        return data
    
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
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неправильный email или пароль")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не активирован")
        self.validated_data['user'] = user
        return data