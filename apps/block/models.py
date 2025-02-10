from django.db import models
from slugify import slugify
# Create your models here.

class Block(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название блока")
    text = models.TextField(verbose_name="Текст блока")
    photo = models.ImageField(upload_to="block_photos", verbose_name="Изображение блока")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")     
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Block.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Блок компании"
        verbose_name_plural = "1. Блок компании"
        ordering = ["-created_at"]
        
class AboutUs(models.Model):
    name = models.CharField(max_length=155, verbose_name="Название")
    test = models.TextField(verbose_name="Текст")
    photo = models.ImageField(upload_to="about_us_photos", verbose_name="Изображение")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="slug", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while AboutUs.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "2. О нас"
        ordering = ["-created_at"]
    