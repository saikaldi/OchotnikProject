from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile, UserAddress, UserPymentCard
from .serializers import UserProfileSerializer, UserAddressSerializer, UserPymentCardSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes 

# Create your views here.

"""Документация для профиля пользователя"""
@extend_schema_view(
    list=extend_schema(
        summary="Список профилей пользователей",
        description="Получение списка всех профилей пользователей",
        responses={200: UserProfileSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получение профиля пользователя",
        description="Получение профиля пользователя по ID",
        responses={200: UserProfileSerializer},
    ),
    create=extend_schema(
        summary="Создание профиля пользователя",
        description="Создание нового профиля пользователя",
        request=UserProfileSerializer,
        responses={201: UserProfileSerializer},
    ),
    update=extend_schema(
        summary="Обновление профиля пользователя",
        description="Полное обновление профиля пользователя по ID",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление профиля пользователя",
        description="Частичное обновление профиля пользователя по ID",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
    ),
    destroy=extend_schema(
        summary="Удаление профиля пользователя",
        description="Удаление профиля пользователя по ID",
        responses={204: None},
    ),
)
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        return UserProfile.objects.filter(user=self.request.user)

    
        # """Документация для адреса пользователя"""
@extend_schema_view(
    list=extend_schema(
        summary="Список адресов пользователя",
        description="Получение списка всех адресов пользователя",
        responses={200: UserAddressSerializer(many=True)},  
    ),
    retrieve=extend_schema(
        summary="Получение адреса пользователя",
        description="Получение адреса пользователя по ID",
        responses={200: UserAddressSerializer},
    ),
    create=extend_schema(
        summary="Создание адреса пользователя",
        description="Создание нового адреса пользователя",
        request=UserAddressSerializer,
        responses={201: UserAddressSerializer},
    ),
    update=extend_schema(
        summary="Обновление адреса пользователя",
        description="Полное обновление адреса пользователя по ID",
        request=UserAddressSerializer,
        responses={200: UserAddressSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление адреса пользователя",
        description="Частичное обновление адреса пользователя по ID",
        request=UserAddressSerializer,
        responses={200: UserAddressSerializer},
    ),
    destroy=extend_schema(
        summary="Удаление адреса пользователя",
        description="Удаление адреса пользователя по ID",
        responses={204: None},
    ),    
)
class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): 
        return UserAddress.objects.filter(user=self.request.user)
  
    #"""Документация для карты пользователя"""
@extend_schema_view(
    list=extend_schema(
        summary="Список карт пользователя",
        description="Получение списка всех карт пользователя",
        responses={200: UserPymentCardSerializer(many=True)},  
    ),
    retrieve=extend_schema(
        summary="Получение карты пользователя",
        description="Получение карты пользователя по ID",
        responses={200: UserPymentCardSerializer},
    ),
    create=extend_schema(
        summary="Создание карты пользователя",
        description="Создание новой карты пользователя",
        request=UserPymentCardSerializer,
        responses={201: UserPymentCardSerializer},
    ),
    update=extend_schema(
        summary="Обновление карты пользователя",
        description="Полное обновление карты пользователя по ID",
        request=UserPymentCardSerializer,
        responses={200: UserPymentCardSerializer},
    ),
    partial_update=extend_schema(
        summary="Частичное обновление карты пользователя",
        description="Частичное обновление карты пользователя по ID",
        request=UserPymentCardSerializer,
        responses={200: UserPymentCardSerializer},
    ),
    destroy=extend_schema(
        summary="Удаление карты пользователя",
        description="Удаление карты пользователя по ID",
        responses={204: None},
    ),    
)
class UserPymentCardViewSet(viewsets.ModelViewSet):
    queryset = UserPymentCard.objects.all()
    serializer_class = UserPymentCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        return UserPymentCard.objects.filter(user=self.request.user)

