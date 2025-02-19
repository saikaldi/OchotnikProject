from django.contrib import admin
from .models import Category, Product, Cart, FavoriteProduct, Review
from slugify import slugify
# Register your models here.
def generate_unique_slug(model, slug_field, source_field, instance):
    if not getattr(instance, slug_field):
        source_value = getattr(instance, source_field)
        if hasattr(source_value, 'username'):
            source_value = source_value.username
        
        slug = slugify(source_value)
        i = 1
        while model.objects.filter(**{slug_field: slug}).exists():
            slug = f"{slugify(source_value)}-{i}"
            i += 1
        setattr(instance, slug_field, slug)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "brand", "model", "price", "is_discount", "quantity", "is_new", "discount_percent", "discount_price", "created_at", "updated_at")
    search_fields = ("product_name", "brand", "model", "price", "is_discount", "quantity", "is_new", "discount_percent", "discount_price", "created_at")
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "product_name", obj)
        super().save_model(request, obj, form, change)
        
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "created_at", "updated_at")
    search_fields = ("category_name",)
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "category_name", obj)
        super().save_model(request, obj, form, change)
    
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity",  "total_price", "created_at", "updated_at")
    search_fields = ("user", "product", "quantity", "total_price", "created_at")
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "user", obj)
        super().save_model(request, obj, form, change)

class FavoriteProductAdmin(admin.ModelAdmin):   
    list_display = ("id", "user", "product_id", "created_at") 
    search_fields = ("user", "product_id",)
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "user", obj)        
        super().save_model(request, obj, form, change) 
 
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product_id", "rating", "created_at", "updated_at")
    search_fields = ("user", "product_id", "rating",)
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "user", obj)
        super().save_model(request, obj, form, change) 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)  
admin.site.register(Cart, CartAdmin)
admin.site.register(FavoriteProduct, FavoriteProductAdmin)
admin.site.register(Review, ReviewAdmin)