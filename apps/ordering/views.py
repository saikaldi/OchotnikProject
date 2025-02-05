from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, Payment, PaymentService
from .serializers import OrderSerializer, OrderDetailSerializer, PaymentSerializer, PaymentServiceSerializer
from ..products.models import Product
from ..products.serializers import ProductSerializer, CartSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):  
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class PaymentServiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentService.objects.all()
    serializer_class = PaymentServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PaymentService.objects.filter(user=self.request.user)