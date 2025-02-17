from django.db import models
from slugify import slugify
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=255, verbose_name="Пол", choices=(('None', 'Нет',), ( 'M', 'Мужской'), ('Ж', 'Женский')))
    phone_number = models.CharField("Номер телефона", max_length=55,
                                validators=[RegexValidator(regex=r"^(0\d{9}|\+996\d{9})$",
                                message="Введите правильный номер телефона")],)
    email = models.EmailField(max_length=255, verbose_name="Email", unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(f"{self.user.username}")
            self.slug = base_slug
            unique_slug = base_slug
            counter = 1
            while UserProfile.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        self.email = self.user.email
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        self.birth_date = self.user.date_joined
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "1. Профили"
        ordering = ["-created_at"]

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    country = models.CharField(max_length=255, verbose_name="Страна")
    city = models.CharField(max_length=255, verbose_name="Город")
    district = models.CharField(max_length=255, verbose_name="Район")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=255, verbose_name="Номер дома")
    flat_number = models.CharField(max_length=255, verbose_name="Номер квартиры")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.user.username} - {self.city} {self.district} {self.street} {self.house_number} {self.flat_number}"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(f"{self.user.username}")
            self.slug = base_slug
            unique_slug = base_slug
            counter = 1
            while UserAddress.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "2. Адреса"
        ordering = ["-created_at"]
        
class UserPymentCard(models.Model):
    cart_regex = RegexValidator(regex=r'^\d{12}$', message="Номер карты должен состоять из 12 цифр")
    cvv = RegexValidator(regex=r'^\d{3}$', message="CVV должен состоять из 3 цифр")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    card = models.CharField(max_length=12, verbose_name="Номер карты", validators=[cart_regex])
    cardholder_name = models.CharField(max_length=255, verbose_name="Имя владельца")
    expiration_date = models.DateField(verbose_name="Дата окончания срока действия")
    cvv = models.CharField(max_length=3, verbose_name="CVV", validators=[cvv])
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.user.username} - {self.card} {self.cardholder_name} {self.expiration_date}"
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(f"{self.user.username}")
            self.slug = base_slug
            unique_slug = base_slug
            counter = 1
            while UserPymentCard.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Карта пользователя"
        verbose_name_plural = "3. Карты ползователя"
        ordering = ["-created_at"]

    

    
    