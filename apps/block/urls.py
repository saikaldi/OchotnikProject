from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockViewSet, AboutUsViewSet

router = DefaultRouter()
router.register(r'blocks', BlockViewSet, basename='block')
router.register(r'about-us', AboutUsViewSet, basename='about-us')

urlpatterns = router.urls