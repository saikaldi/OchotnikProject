from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockViewSet, AboutUsViewSet

router = DefaultRouter()
router.register(r"blogs", BlockViewSet, basename="blogs")
router.register(r"about", AboutUsViewSet, basename="about")

urlpatterns = router.urls
