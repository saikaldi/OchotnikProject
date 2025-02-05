from rest_framework import viewsets

from .models import UserProfile, UserAddress, UserPymentCard
from .serializers import UserProfileSerializer, UserAddressSerializer, UserPymentCardSerializer
# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    
class UserPymentCardViewSet(viewsets.ModelViewSet):
    queryset = UserPymentCard.objects.all()
    serializer_class = UserPymentCardSerializer