from django.contrib import admin
from .models import UserProfile, UserAddress, UserPymentCard
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

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "birth_date", "gender", "phone_number")
    search_fields = ("user__username", "first_name", "last_name", "phone_number")
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "user", obj)
        super().save_model(request, obj, form, change)        
        
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "country", "city", "district", "street", "house_number", "flat_number")
    search_fields = ("user", "country", "city","district", "street", "house_number", "flat_number" ) 
    exclude = ("slug",) 
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "user", obj)
        super().save_model(request, obj, form, change)
        
class UserPymentCardAdmin(admin.ModelAdmin):    
    list_display = ("id", "user", "card", "cardholder_name", "expiration_date", "cvv")
    search_fields = ("user", "cart", "cartholder_name",)
    exclude = ("slug",)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, "slug", "user", obj)
        super().save_model(request, obj, form, change)  # Не забудьте вызвать super()

            
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress,UserAddressAdmin)
admin.site.register(UserPymentCard, UserPymentCardAdmin)