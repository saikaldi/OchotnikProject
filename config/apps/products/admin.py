from django.contrib import admin
from .models import Category, Product, Cart, FavoriteProduct

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "brand", "model", "price", "is_discount", "quantity", "is_new", "discount_percent", "discount_price", "created_at")
    prepopulated_fields = {"slug": ("product_name",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("category_name",)}
    
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity",  "total_price", "created_at")

class FavoriteProductAdmin(admin.ModelAdmin):   
    list_display = ("user", "product_id", "created_at") 
    prepopulated_fields = {"slug": ("product_id",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)  
admin.site.register(Cart, CartAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)