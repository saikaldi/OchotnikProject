from rest_framework import viewsets
from .models import Block, AboutUs
from .serializers import BlockSerializer, AboutUsSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="Список блоков",
        description="Получение списка всех блоков",
        responses={
            200: OpenApiResponse(
                response=BlockSerializer(many=True),
                description="Список блоков"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение блока",
        description="Получение блока по ID",
        responses={
            200: OpenApiResponse(
                response=BlockSerializer,
                description="Блок"
            )
        },
    ),
)
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer  
    
@extend_schema_view(
    list=extend_schema(
        summary="Список о нас",
        description="Получение списка всех о нас",
        responses={
            200: OpenApiResponse(
                response=AboutUsSerializer(many=True),
                description="Список о нас"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение о нас",
        description="Получение о нас по ID",
        responses={
            200: OpenApiResponse(
                response=AboutUsSerializer,
                description="О нас"
            )
        },
    ),
)
    
class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    