from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CartViewSet, FavoriteProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)       
router.register(r"cart", CartViewSet)
router.register(r"favorite-products", FavoriteProductViewSet)
router.register(r"reviews", ReviewViewSet)
urlpatterns = [
    path("", include(router.urls)),
]