from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Cart, FavoriteProduct, Review
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, FavoriteProductSerializer, ReviewSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter

#"""Документация для категории"""
@extend_schema(
    summary="Категория товаров",
    description="Api для создания категории товаров",
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={
                "category_name": "название категори товаров",
            },
            request_only=True
        )
    ]
)
@extend_schema(tags=['Products category: Категория товаров'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список товаров по категории",
        description="Получение списка всех",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer(many=True),
                description="Список товаров"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение товара c отзывами и похожими товарами",
        description="Получение товара по ID"
    )
)
@extend_schema(tags=['Products:Список товаров'])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()    
    serializer_class = ProductSerializer
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product_serializer = ProductSerializer(product)
        review_serializer = ReviewSerializer([review for review in product.review_set.all()], many=True)
        similar_products_serializer = ProductSerializer([similar_product for similar_product in product.similar_products()], many=True)
        return Response(
                        {"product": product_serializer.data, 
                        "reviews": review_serializer.data, 
                        "similar_products": similar_products_serializer.data}
                        )
      
@extend_schema_view(
    list=extend_schema(
        summary="Список корзин",
        description="Получение списка всех корзин пользователей.",
        responses={
            200: OpenApiResponse(
                response=CartSerializer(many=True),
                description="Список корзин успешно получен.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value=[
                            {
                                "id": 1,
                                "user_id": 1,   
                                "product_id": 3,
                                "quantity": 10,
                                "total_price": 100,
                            },
                            {
                                "id": 2,
                                "user_id": 1,
                                "product": 4,
                                "quantity": 10,
                                "total_price": 5000,
                            },
                        ],
                    )
                ],
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение корзины по ID",
        description="Получение деталей корзины по её уникальному идентификатору.",
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Корзина успешно получена.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": ("ID корзины ", 1),
                            "user": ("ID пользователя ", 1),
                            "product": ("ID товара ", 3),
                            "quantity": ("Количество товара ", 10),
                            "total_price":("Общая стоимость товара ", 100),
                        },
                    )
                ],
            ),
            404: OpenApiResponse(
                description="Корзина с указанным ID не найдена.",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание корзины",
        description="Создание новой корзины для пользователя.",
        request=CartSerializer,
        responses={
            201: OpenApiResponse(
                response=CartSerializer,
                description="Корзина успешно создана.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product": 3,
                            "quantity": 10,
                            "total_price": 100,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "user": 1,
                    "product": 3,
                    "quantity": 10,
                },
            )
        ],
    ),
    update=extend_schema(
        summary="Обновление корзины",
        description="Полное обновление данных корзины по её ID.",
        request=CartSerializer,
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Корзина успешно обновлена.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product": 3,
                            "quantity": 15,
                            "total_price": 150,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
            404: OpenApiResponse(
                description="Корзина с указанным ID не найдена.",
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "user": 1,
                    "product": 3,
                    "quantity": 15,
                },
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление корзины",
        description="Частичное обновление данных корзины по её ID.",
        request=CartSerializer,
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Корзина успешно обновлена.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product": 3,
                            "quantity": 15,
                            "total_price": 150,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
            404: OpenApiResponse(
                description="Корзина с указанным ID не найдена.",
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "quantity": 15,
                },
            )
        ],
    ),
    destroy=extend_schema(
        summary="Удаление корзины",
        description="Удаление корзины по её ID.",
        responses={
            204: OpenApiResponse(
                description="Корзина успешно удалена.",
            ),
            404: OpenApiResponse(
                description="Корзина с указанным ID не найдена.",
            ),
        },
    ),
)
@extend_schema(tags=["Cart: Корзина пользователя"])
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()   
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user=request.user)
        carts_serializer = CartSerializer(carts, many=True)
        products_serializer = ProductSerializer([cart.product for cart in carts], many=True)
        for cart, product in zip(carts_serializer.data, products_serializer.data):
            cart['product'] = product
        cart_total_price = sum([cart.cart_total_price() for cart in carts])
        return Response({"carts": carts_serializer.data, "cart_total_price": cart_total_price})
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_serializer = CartSerializer(cart)
        product_serializer = ProductSerializer(cart.product)
        return Response({"cart": cart_serializer.data, "product": product_serializer.data})
   
"""Документация для избранного товара"""
@extend_schema_view(
    list=extend_schema(
        summary="Список избранных товаров",
        description="Получение списка всех избранных товаров",
        responses={
            200: OpenApiResponse(
                response=FavoriteProductSerializer(many=True),
                description="Список избранных товаров",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value=[
                            {
                                "id": 1,
                                "user": 1,
                                "product_id": 3,
                            
                            },
                            {
                                "id": 2,
                                "user": 1,
                                "product_id": 4,
                            },
                        ],
                    )
                ],
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получение избранного товара",
        description="Получение избранного товара по ID",
        responses={
            200: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product_id": 3,
                        },
                    )
                ],
            ),
            404: OpenApiResponse(
                description="Избранный товар с указанным ID не найден.",
            ),
        },
    ),
    create=extend_schema(
        summary="Создание избранного товара",
        description="Создание нового избранного товара",
        request=FavoriteProductSerializer,
        responses={
            201: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product_id": 3,
                        },
                    )
                ],
            ),            
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "user": 1,
                    "product_id": 3,
                },
            )
        ],        
    ),
    update=extend_schema(
        summary="Обновление избранного товара",
        description="Полное обновление избранного товара по его ID",
        request=FavoriteProductSerializer,                
        responses={
            200: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product_id": 3,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
            404: OpenApiResponse(
                description="Избранный товар с указанным ID не найден.",
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "user": 1,
                    "product_id": 3,
                },
            )
        ],
    ),
    destroy=extend_schema(
        summary="Удаление избранного товара",
        description="Удаление избранного товара по его ID.",
        responses={
            204: OpenApiResponse(
                description="Избранный товар успешно удален.",
            ),
            404: OpenApiResponse(
                description="Избранный товар с указанным ID не найден.",
            ),
        },
    ),      
)
@extend_schema(tags=["FavoriteProduct: Избранные товары"])
class FavoriteProductViewSet(viewsets.ModelViewSet):
    queryset = FavoriteProduct.objects.all()    
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        favorite_products = FavoriteProduct.objects.filter(user=self.request.user)
        favorite_products_serializer = FavoriteProductSerializer(favorite_products, many=True)
        products_serializer = ProductSerializer([favorite_product.product_id for favorite_product in favorite_products], many=True)
        for favorite_product, product in zip(favorite_products_serializer.data, products_serializer.data):
            favorite_product['product'] = product
        return Response({"favorite_products": favorite_products_serializer.data})
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        favorite_product = get_object_or_404(FavoriteProduct, pk=pk, user=self.request.user)
        favorite_product_serializer = FavoriteProductSerializer(favorite_product)
        product_serializer = ProductSerializer(favorite_product.product_id)
        return Response({"favorite_product": favorite_product_serializer.data, "product": product_serializer.data})
 
"""Документация для отзыва"""
@extend_schema_view(
    list=extend_schema(
        summary="Список отзывов", 
        description="Получение списка всех отзывов", 
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer(many=True),
                description="Список отзывов"
            )
        },
        examples=[
            OpenApiExample(
                "Пример ответа",
                value=[
                    {
                        "id": 1,
                        "user": 1,
                        "product_id": 3,
                        "text": "Отличный товар",
                        "rating": ("**"),
                        "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                        "created_at": "2023-05-25T13:27:53.020Z",
                    },
                    {
                        "id": 2,
                        "user": 1,
                        "product_id": 4,
                        "text": "Хороший товар",
                        "rating": ("***"),
                        "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                        "created_at": "2023-05-25T13:27:53.020Z",
                    },
                ],
            )
        ],  
    ),
    retrieve=extend_schema(
        summary="Получение отзыва",
        description="Получение отзыва по его ID",
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Отзыв"
            )
        },
        examples=[
            OpenApiExample(
                "Пример ответа",
                value={
                    "id": 1,
                    "user": 1,
                    "product_id": 3,
                    "text": "Отличный товар",
                    "rating": ("*****"),
                    "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                    "created_at": "2023-05-25T13:27:53.020Z",
                },
            )
        ],
    ),
    create=extend_schema(
        summary="Создание отзыва",  
        description="Создание нового отзыва",
        request=ReviewSerializer,
        responses={
            201: OpenApiResponse(
                response=ReviewSerializer,
                description="Отзыв",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product_id": 3,
                            "text": "Отличный товар",
                            "rating": ("****"),
                            "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                            "created_at": "2023-05-25T13:27:53.020Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "user": 1,
                    "product_id": 3,
                    "text": "Отличный товар",
                    "rating": ("****"),
                    "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                },
            )
        ],
    ),
    update=extend_schema(
        summary="Обновление отзыва",
        description="Полное обновление отзыва по его ID",   
        request=ReviewSerializer,
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,                
                description="Отзыв",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product_id": 3,
                            "text": "Отличный товар",
                            "rating": ("***"),
                            "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                            "created_at": "2023-05-25T13:27:53.020Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
            404: OpenApiResponse(
                description="Отзыв с указанным ID не найден.",
            ),
        },
    ),
    partial_update=extend_schema(   
        summary="Частичное обновление отзыва",
        description="Частичное обновление отзыва по его ID",
        request=ReviewSerializer,
        responses={
            200: OpenApiResponse(                
                response=ReviewSerializer,
                description="Отзыв",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 1,
                            "user": 1,
                            "product_id": 3,
                            "text": "Отличный товар",
                            "rating": ("***"),
                            "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                            "created_at": "2023-05-25T13:27:53.020Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Некорректные данные в запросе.",
            ),
            404: OpenApiResponse(
                description="Отзыв с указанным ID не найден.",
            ),  
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "user": 1,
                    "product_id": 3,
                    "text": "Отличный товар",
                    "rating": 5,
                    "photo": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                },
            )
        ],
    ),
    destroy=extend_schema(
        summary="Удаление отзыва",
        description="Удаление отзыва по его ID.",
        responses={
            204: OpenApiResponse(
                description="Отзыв успешно удален.",
            ),
            404: OpenApiResponse(
                description="Отзыв с указанным ID не найден.",
            ),
        },
    ),  
)   
@extend_schema(tags=["Review: Отзывы пользователей"])
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()    
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)