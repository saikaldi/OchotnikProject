from django.contrib import admin
from .models import User, EmailVerification
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',  'user_status','is_staff', 'is_active', 'date_joined', 'last_login')
    search_fields = ('email', )
    
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'created_at', 'is_used')
    search_fields = ('user',)
    
admin.site.register(User, UserAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)