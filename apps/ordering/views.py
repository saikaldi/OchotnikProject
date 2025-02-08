from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, Payment, PaymentService
from .serializers import OrderSerializer, OrderDetailSerializer, PaymentSerializer, PaymentServiceSerializer
from ..products.models import Product
from ..products.serializers import ProductSerializer, CartSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter

# Create your views here.

#"""Документация для заказа"""
@extend_schema_view(
    list=extend_schema(
        summary="Список заказов",
        description="Получение списка всех заказов",
        responses={200: OrderSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получение заказа",
        description="Получение заказа по ID",
        responses={200: OrderSerializer},
    ),
    create=extend_schema(
        summary="Создание заказа",
        description="Создание нового заказа",
        request=OrderSerializer,
        responses={201: OrderSerializer},
    ),
    update=extend_schema(
        summary="Обновление заказа",
        description="Полное обновление заказа по ID",
        request=OrderSerializer,
        responses={200: OrderSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление заказа",
        description="Частичное обновление заказа по ID",
        request=OrderSerializer,
        responses={200: OrderSerializer},
    ),
    destroy=extend_schema(
        summary="Удаление заказа",
        description="Удаление заказа по ID",
        responses={204: None},
    ),
)
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
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
#"""Документация для оплаты"""
@extend_schema_view(
    list=extend_schema(
        summary="Список оплат",
        description="Получение списка всех оплат",
        responses={200: PaymentSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получение оплаты",
        description="Получение оплаты по ID",
        responses={200: PaymentSerializer},
    ),
    create=extend_schema(
        summary="Создание оплаты",
        description="Создание новой оплаты",
        request=PaymentSerializer,
        responses={201: PaymentSerializer},
    ),
    update=extend_schema(
        summary="Обновление оплаты",
        description="Полное обновление оплаты по ID",
        request=PaymentSerializer,
        responses={200: PaymentSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление оплаты",
        description="Частичное обновление оплаты по ID",
        request=PaymentSerializer,
        responses={200: PaymentSerializer},
    ),
    destroy=extend_schema(
        summary="Удаление оплаты",
        description="Удаление оплаты по ID",
        responses={204: None},
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
#"""""Документация для сервиса оплаты"""
@extend_schema_view(
    list=extend_schema(
        summary="Список сервисов оплаты",
        description="Получение списка всех сервисов оплаты",
        responses={200: PaymentServiceSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получение сервиса оплаты",
        description="Получение сервиса оплаты по ID",
        responses={200: PaymentServiceSerializer},
    ),
    create=extend_schema(
        summary="Создание сервиса оплаты",
        description="Создание нового сервиса оплаты",
        request=PaymentServiceSerializer,
        responses={201: PaymentServiceSerializer},
    ),
    update=extend_schema(
        summary="Обновление сервиса оплаты",
        description="Полное обновление сервиса оплаты по ID",
        request=PaymentServiceSerializer,
        responses={200: PaymentServiceSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление сервиса оплаты",        
        description="Частичное обновление сервиса оплаты по ID",
        request=PaymentServiceSerializer,
        responses={200: PaymentServiceSerializer},
    ),
    destroy=extend_schema(
        summary="Удаление сервиса оплаты",
        description="Удаление сервиса оплаты по ID",
        responses={204: None},
    ),
)
class PaymentServiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentService.objects.all()
    serializer_class = PaymentServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PaymentService.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)