from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.db import models
import random


# Кастомный менеджер модели пользователя
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Пользователь должен иметь email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_status", "Админ")
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('Админ', 'Админ'),
        ('Менеджер', 'Менеджер'),
        ('Пользователь', 'Пользователь'),
    ]
    frist_name = models.CharField(max_length=50, verbose_name="Имя", blank=True, null=True) 
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", blank=True, null=True)
    user_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Пользователь", blank=True, null=True, verbose_name="Статус")
    email = models.EmailField(unique=True, verbose_name="Email")
    is_staff = models.BooleanField(default=False)                # Флаг для статуса администратора
    is_active = models.BooleanField(default=False)               # Флаг для активности пользователя
    date_joined = models.DateTimeField(default=timezone.now)     # Дата регистрации
    last_login = models.DateTimeField(default=timezone.now)      # Последний вход
    
    objects = UserManager()                                      # Менеджер пользователей
    USERNAME_FIELD = "email"                                    # Имя поля для пользователя
    REQUIRED_FIELDS = []                                 # Требуемые поля для регистрации
    
    
    def __str__(self):
        return f'{self.id} - {self.email}'
    
    @property
    def is_admin(self):                                          # Проверка администратора
        return self.user_status == 'Админ'
    
    @property
    def is_manager(self):                                        # Проверка менеджера
        return self.user_status == 'Менеджер'
    
    @property
    def is_user(self):                                           # Проверка пользователя
        return self.user_status == 'Пользователь'
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        

class EmailVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    code = models.CharField(max_length=6, verbose_name="Код подтверждения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_used = models.BooleanField(default=False, verbose_name="Использован")
    
    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789', k=6))
    
    # Функция проверки времени жизни кода
    def is_expired(self):
        return self.created_at + timedelta(minutes=3) < timezone.now()
   
    def __str__(self):
        return f'{self.user.email} - {self.code}'
    
    class Meta:
        verbose_name = "Подтверждение по email"
        verbose_name_plural = "Подтверждения по email"