from django.contrib import admin
from .models import User, EmailVerification
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_status','is_staff', 'is_active', 'date_joined', 'last_login')
    
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    
admin.site.register(User, UserAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)