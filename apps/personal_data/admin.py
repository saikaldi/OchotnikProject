from django.contrib import admin
from .models import UserProfile, UserAddress, UserPymentCard
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "birth_date", "gender", "phone_number", "email")
    prepopulated_fields = {"slug": ("user",)}
    
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "city", "district", "street", "house_number", "flat_number")
    prepopulated_fields = {"slug": ("user",)}
    
class UserPymentCardAdmin(admin.ModelAdmin):    
    list_display = ("user", "card", "cardholder_name", "expiration_date", "cvv")
    preserve_filters = {"slug": ("user",)}
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress,UserAddressAdmin)
admin.site.register(UserPymentCard, UserPymentCardAdmin)