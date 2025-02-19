from django.contrib import admin
from .models import Order, PaymentService, Payment
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

class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'user', 'cart', 'address', 'status', 'quantity', 'total_sum', 'date', 'updated_at') 
    search_fields = ('user', 'cart', 'address', 'status', 'date')
    exclude = ('slug',)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, 'slug', 'user', obj)
        super().save_model(request, obj, form, change)

class PaymentServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_service_name', 'created_at', 'updated_at')
    search_fields = ('payment_service_name',)
    exclude = ('slug',)
    
    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, 'slug', 'payment_service_name', obj)
        super().save_model(request, obj, form, change)
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'address', 'amount', 'status', 'created_at', 'updated_at')
    exclude = ('slug',)

    def save_model(self, request, obj, form, change):
        generate_unique_slug(self.model, 'slug', 'user', obj)
        super().save_model(request, obj, form, change)
    
admin.site.register(PaymentService, PaymentServiceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)

