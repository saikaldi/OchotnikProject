from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from ..products.models import Cart
from ..personal_data.models import UserAddress, UserPymentCard
from django.core.mail import send_mail


# Create your models here.
class PaymentService(models.Model):
    payment_service_name = models.CharField(max_length=100, verbose_name="Название сервиса оплаты")
    photo = models.ImageField(verbose_name="Изображение", upload_to="payment_services/images")
    qr_code = models.ImageField(upload_to='payment_qr_codes/images', verbose_name="QR-код")
    prop_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер реквезита')  # Номер реквизита
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя Владельца карты')
    whatsapp_url = models.TextField(blank=True, null=True, verbose_name='Ссылка на WhatsApp')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return self.payment_service_name
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":            
            base_slug = slugify(self.payment_service_name)
            unique_slug = base_slug
            counter = 1
            while PaymentService.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Сервис оплаты"
        verbose_name_plural = "1. Сервисы оплаты"
        ordering = ["-created_at"]


class Order(models.Model):
    CHOICES_STATUS = (
        ('Оформлено', 'Оформлено'),
        ('Оплачено', 'Оплачено'),
        ('Отменено', 'Отменено'),
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    cart = models.ForeignKey(Cart,  on_delete=models.CASCADE, related_name='orders', verbose_name='Корзина товаров')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders', blank=True, null=True, verbose_name='Адрес доставки')
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default='Оформлено', verbose_name='Статус заказа')
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total_sum = models.DecimalField(max_digits=10, decimal_places=2,  verbose_name='Сумма заказа', default=1)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):  
        return f'Заказ {self.id} - {self.user.username}'
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.user.username)
            unique_slug = base_slug
            counter = 1
            while Order.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        self.quantity = self.cart.quantity          
        self.total_sum = self.cart.total_price
        if self.status == 'Оформлено':
            send_mail(
                'Ваш заказ на обработке',
                'оплатите что бы получить свой товар!',
                'admin@example.com',
                [self.user.email],
                fail_silently=False,
            )

        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "2. Заказы"
        ordering = ["-created_at"]
        
class Payment(models.Model):
    CHOICES_STATUS = (
        ('Оплачено', 'Оплачено'),
        ('Отменено', 'Отменено'),
        ('Выполнено', 'Выполнено'),
        ('Не выполнено', 'Не выполнено'),
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_service = models.ForeignKey(PaymentService, on_delete=models.CASCADE, related_name='payments', verbose_name='Сервис оплаты')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='Заказ')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='payments', blank=True, null=True, verbose_name='Адрес доставки')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default='Оплачено', verbose_name='Статус оплаты')
    slug = models.SlugField(max_length=200, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')      
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return f'Оплата {self.id} - {self.user.username}'
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.user.username)
            unique_slug = base_slug
            counter = 1
            while Payment.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug   
        if self.status == 'Оплачено':
            send_mail(
                'Ваш оплата принята!',
                'Ваш заказ уже на дороге!',
                'admin@example.com',
                [self.user.email],
                fail_silently=False,
            )
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "2. Оплаты"   
        ordering = ["-created_at"]
        

    
