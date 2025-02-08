from rest_framework import viewsets
from .models import Block
from .serializers import BlockSerializer
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
    