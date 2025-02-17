from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile, UserAddress, UserPymentCard
from .serializers import UserProfileSerializer, UserAddressSerializer, UserPymentCardSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes 

# Create your views here.

"""Документация для профиля пользователя"""
@extend_schema(
    summary="Профиль пользователя",
    description="Профиль пользователя",
    request=UserProfileSerializer,
    responses={
        200: OpenApiResponse(
            description="Профиль пользователя успешно создан",
            examples=[OpenApiExample("Профиль пользователя успешно создан", value={"message": "Профиль пользователя успешно создан."})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[OpenApiExample("Ошибка валидации, поле email уже используется", value={"email": ["Этот email уже используется"]})]
        )
    }
)
@extend_schema(tags=['UserProfile: Профиль пользователя'])
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        return UserProfile.objects.filter(user=self.request.user)

    
        # """Документация для адреса пользователя"""
@extend_schema(
    summary="Адрес пользователя",
    description="Адрес пользователя",
    request=UserAddressSerializer,
    responses={
        200: OpenApiResponse(
            description="Адрес пользователя успешно создан",
            examples=[OpenApiExample("Адрес пользователя успешно создан", value={"message": "Адрес пользователя успешно создан."})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[OpenApiExample("Ошибка валидации", value={"email": ["Этот email уже используется"]})]
        )
    },
)
@extend_schema(tags=['UserAddress: Адрес пользователя'])
class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): 
        return UserAddress.objects.filter(user=self.request.user)
  
    #"""Документация для карты пользователя"""
@extend_schema(
    summary="Карта пользователя",
    description="Карта пользователя",
    request=UserPymentCardSerializer,
    responses={
        200: OpenApiResponse(
            description="Карта пользователя успешно создана",
            examples=[OpenApiExample("Карта пользователя успешно создана", value={"message": "Карта пользователя успешно создана."})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[OpenApiExample("Ошибка валидации", value={"email": ["Этот email уже используется"]})]
        )
    },
)
@extend_schema(tags=['UserPymentCard: Карта пользователя'])
class UserPymentCardViewSet(viewsets.ModelViewSet):
    queryset = UserPymentCard.objects.all()
    serializer_class = UserPymentCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        return UserPymentCard.objects.filter(user=self.request.user)

