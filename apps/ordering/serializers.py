from rest_framework import serializers
from .models import Order, Payment, PaymentService
from ..products.serializers import ForCartSerializer
from ..personal_data.serializers import UserAddressSerializer


class OrderSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Order   
        fields = ['id', 'status', 'user', 'cart', 'quantity', 'total_sum', 'address', 'date', 'created_at', 'updated_at']

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'user',  'quantity', 'total_sum', 'address', 'date', 'created_at', 'updated_at']

class OrderDetailSerializer(serializers.ModelSerializer):
    cart = ForCartSerializer()
    address = UserAddressSerializer()
    class Meta:
        model = Order
        fields = ['id', 'status', 'user', 'cart', 'address', 'quantity', 'total_sum', 'date',  'created_at', 'updated_at']
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_service', 'order', 'address', 'amount', 'status', 'created_at', 'updated_at']
        
class PaymentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentService
        fields = ['id', 'payment_service_name', 'photo', 'qr_code', 'prop_number', 'full_name', 'whatsapp_url', 'created_at', 'updated_at']