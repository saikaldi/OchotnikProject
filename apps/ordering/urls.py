from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, PaymentViewSet, PaymentServiceViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders-api')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'payment-services', PaymentServiceViewSet, basename='payment_services')

urlpatterns = router.urls

