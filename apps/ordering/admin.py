from django.contrib import admin
from .models import Order, PaymentService, Payment
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'address', 'status', 'total_sum', 'date', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("user",)}

class PaymentServiceAdmin(admin.ModelAdmin):
    list_display = ('payment_service_name', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("payment_service_name",)}
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'address', 'amount', 'status', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("user",)}
    
admin.site.register(PaymentService, PaymentServiceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)

