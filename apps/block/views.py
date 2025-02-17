from rest_framework import viewsets
from .models import Block, AboutUs
from .serializers import BlockSerializer, AboutUsSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter

# Create your views here.

@extend_schema(
    summary="Блок компании",
    description="Api для создания блока компании",
    tags=['Block: Блок компании'],
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={
                "title": "Название блока",
                "text": "Текст блока",
                "photo": "https://www.example.com/image.jpg",
            },
            request_only=True
        )
    ]
)
class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer  
    
@extend_schema(
    summary="О нас",
    description="Api для создания о нас",
    request=AboutUsSerializer,
    tags=['Block: О нас'],
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={
                "title": "Название публикации",
                "text": "Текст публикации",
                "photo": "https://www.example.com/image.jpg",
            },
            request_only=True
        )
    ]
)
class AboutUsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    