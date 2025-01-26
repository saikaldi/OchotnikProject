from django.db import models
from slugify import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from decimal import Decimal


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.category_name)
            unique_slug = base_slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
            
    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "1. Категории товара"
        ordering = ["-created_at"]
        
        
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория товара")
    product_name = models.CharField(max_length=100, verbose_name="Название товара")
    country = models.CharField(max_length=100, verbose_name="Страна")
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    model = models.CharField(max_length=100, verbose_name="Модель")
    color = models.CharField(max_length=100, verbose_name="Цвет")
    size = models.CharField(max_length=100, verbose_name="Размер")
    material = models.CharField(max_length=100, verbose_name="Материал")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Изображение", upload_to="products/images")
    quantity = models.IntegerField(verbose_name="Количество в запасе")
    is_new = models.BooleanField(default=False, verbose_name="Новый товар")
    is_hot = models.BooleanField(default=False, verbose_name="Горячий товар")   
    is_special = models.BooleanField(default=False, verbose_name="Специальный товар")
    is_promo = models.BooleanField(default=False, verbose_name="Промо товар")
    is_discount = models.BooleanField(default=False, verbose_name="Товар со скидкой", blank=True, null=True)
    discount_percent = models.IntegerField(default=0, verbose_name="Скидка в процентах", blank=True, null=True, validators=[MaxValueValidator(100)])
    discount_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Цена со скидкой", blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.product_name
        
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.product_name)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        if self.is_discount:
             self.discount_price = self.price * (1 - Decimal(self.discount_percent) / 100)
        else:
            self.discount_price = None
            self.discount_percent = 0
        super().save(*args, **kwargs)
  
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "2. Товары"
        ordering = ["-created_at"]

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма заказа", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    
    def save(self, *args, **kwargs):
        if self.product.is_discount:
            self.total_price = self.quantity * self.product.discount_price
        else:   
            self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)
        
    def cart_total_price(self):
        return self.total_price

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "3. Корзина"
        ordering = ['-total_price']
        
        
class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.user.username} - {self.product_id.product_name}"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.product_id.product_name)
            unique_slug = base_slug
            counter = 1
            while FavoriteProduct.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
            
    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "4. Избранные товары"
        ordering = ["-created_at", "user"]
        
        
class Review(models.Model):
    CHOICES_RATING = (
        ('*', '*'),
        ('**', '**'),
        ('***', '***'), 
        ('****', '****'),
        ('*****', '*****'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    text = models.TextField(verbose_name="Текст")
    rating = models.CharField(default='**', max_length=5, choices=CHOICES_RATING, verbose_name="Рейтинг")
    photo = models.ImageField(verbose_name="Изображение", upload_to="reviews/images")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.user.username} - {self.product_id.product_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.text)
            unique_slug = base_slug
            counter = 1
            while Review.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
            
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "5. Отзывы"
        ordering = ["-created_at", "user"]
        