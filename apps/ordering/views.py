from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, Payment, PaymentService
from .serializers import OrderSerializer, OrderDetailSerializer, PaymentSerializer, PaymentServiceSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter

# Create your views here.

#"""Документация для заказа"""
@extend_schema_view(
    list=extend_schema(
        description="Получение списка заказов пользователя",
        responses={200: OpenApiResponse(OrderSerializer(many=True))},
    ),  
    retrieve=extend_schema(
        description="Получение одного заказа пользователя",
        responses={200: OpenApiResponse(OrderSerializer(many=False))},
    ),
    create=extend_schema(
        description="Создание нового заказа пользователя",
        responses={201: OpenApiResponse(OrderSerializer(many=False))},
    ),
    update=extend_schema(
        description="Обновление заказа пользователя",
        responses={200: OpenApiResponse(OrderSerializer(many=False))},
    ),  
    partial_update=extend_schema(
        description="Изменение части заказа пользователя",  
        responses={200: OpenApiResponse(OrderSerializer(many=False))},
    ),
    destroy=extend_schema(
        description="Удаление заказа пользователя",
        responses={204: OpenApiResponse(None)},
    ),
)
@extend_schema(tags=[["Order: Заказ"]])
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
    list=extend_schema(description="Получение списка всех оплат"),  
    retrieve=extend_schema(description="Получение оплаты по ID"),
    create=extend_schema(description="Создание новой оплаты"),
    update=extend_schema(description="Обновление оплаты"),
    partial_update=extend_schema(description="Изменение части оплаты"),  
    destroy=extend_schema(description="Удаление оплаты"),   
)
@extend_schema(tags=[["Payment: Оплата"]])
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
@extend_schema(tags=[["Payment: Сервис оплаты"]])
class PaymentServiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentService.objects.all()
    serializer_class = PaymentServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PaymentService.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)