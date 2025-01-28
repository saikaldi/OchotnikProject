from django.contrib import admin
from .models import Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'date', 'total_price', 'total_discount', 'total_sum')

admin.site.register(Order, OrderAdmin)

