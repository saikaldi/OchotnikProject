from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserAddressViewSet, UserPymentCardViewSet

router = DefaultRouter()
router.register(r"user-profile", UserProfileViewSet)
router.register(r"user-address", UserAddressViewSet)
router.register(r"user-pyment-card", UserPymentCardViewSet)

urlpatterns = [
    path("", include(router.urls)),
]