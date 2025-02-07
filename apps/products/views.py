from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Cart, FavoriteProduct, Review
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, FavoriteProductSerializer, ReviewSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter

#"""Документация для категории"""
@extend_schema_view(
    list=extend_schema(
        summary="Список категорий",
        description="Получение списка всех категорий",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer(many=True),
                description="Список категорий"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение категории",
        description="Получение категории по ID",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Категория"
            )
        },
    ),
    create=extend_schema(
        summary="Создание категории",
        description="Создание новой категории",
        request=CategorySerializer,
        responses={
            201: OpenApiResponse(
                response=CategorySerializer,
                description="Категория"
            )
        },
    ),
    update=extend_schema(
        summary="Обновление категории",
        description="Полное обновление категории по ID",
        request=CategorySerializer,
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Категория"
            )
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление категории",
        description="Частичное обновление категории по ID",
        request=CategorySerializer,
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Категория"
            )
        },
    ),
    destroy=extend_schema(
        summary="Удаление категории",
        description="Удаление категории по ID",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Категория удалена"
            )
        },
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список товаров",
        description="Получение списка всех товаров",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer(many=True),
                description="Список товаров"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение товара  с коментариями и похожими товарами",
        description="Получение товара по ID",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer,
                description="Товар"
            )
        },
    ),
    create=extend_schema(
        summary="Создание товара",
        description="Создание нового товара",
        request=ProductSerializer,
        responses={
            201: OpenApiResponse(
                response=ProductSerializer,
                description="Товар"
            )
        },
    ),
    update=extend_schema(
        summary="Обновление товара",
        description="Полное обновление товара по ID",
        request=ProductSerializer,
        responses={
            200: OpenApiResponse(
                response=ProductSerializer,
                description="Товар"
            )
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление товара",
        description="Частичное обновление товара по ID",
        request=ProductSerializer,
        responses={
            200: OpenApiResponse(
                response=ProductSerializer,
                description="Товар"
            )
        },
    ),
    destroy=extend_schema(
        summary="Удаление товара",
        description="Удаление товара по ID",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Товар удален"
            )
        },
    ),
)
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
      
"""Документация для корзины"""
@extend_schema_view(
    list=extend_schema(
        summary="Список корзин",
        description="Получение списка всех корзин",
        responses={
            200: OpenApiResponse(
                response=CartSerializer(many=True),
                description="Список корзин"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение корзины",
        description="Получение корзины по ID",
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Корзина"
            )
        },
    ),
    create=extend_schema(
        summary="Создание корзины",
        description="Создание новой корзины",
        request=CartSerializer,
        responses={
            201: OpenApiResponse(
                response=CartSerializer,
                description="Корзина"
            )
        },
    ),
    update=extend_schema(
        summary="Обновление корзины",
        description="Полное обновление корзины по ID",
        request=CartSerializer,
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Корзина"
            )
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление корзины",
        description="Частичное обновление корзины по ID",
        request=CartSerializer,
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Корзина"
            )
        },
    ),
    destroy=extend_schema(
        summary="Удаление корзины",
        description="Удаление корзины по ID",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Корзина удалена"
            )
        },
    ),
)
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()   
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

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
                description="Список избранных товаров"
            )
        },
    ),
    retrieve=extend_schema(
        summary="Получение избранного товара",
        description="Получение избранного товара по ID",
        responses={
            200: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар"
            )
        },
    ),
    create=extend_schema(
        summary="Создание избранного товара",
        description="Создание нового избранного товара",
        request=FavoriteProductSerializer,
        responses={
            201: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар"
            )
        },
    ),
    update=extend_schema(
        summary="Обновление избранного товара",
        description="Полное обновление избранного товара по ID",
        request=FavoriteProductSerializer,
        responses={
            200: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар"
            )
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление избранного товара",
        description="Частичное обновление избранного товара по ID",
        request=FavoriteProductSerializer,
        responses={
            200: OpenApiResponse(
                response=FavoriteProductSerializer,
                description="Избранный товар"
            )
        },
    ),
    destroy=extend_schema(
        summary="Удаление избранного товара",
        description="Удаление избранного товара по ID",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Избранный товар удален"
            )
        },
    ),
)
class FavoriteProductViewSet(viewsets.ModelViewSet):
    queryset = FavoriteProduct.objects.all()    
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)

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
    ),
    retrieve=extend_schema(
        summary="Получение отзыва",
        description="Получение отзыва по ID",
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Отзыв"
            )
        },
    ),
    create=extend_schema(
        summary="Создание отзыва",
        description="Создание нового отзыва",
        request=ReviewSerializer,
        responses={
            201: OpenApiResponse(
                response=ReviewSerializer,
                description="Отзыв"
            )
        },
    ),
    update=extend_schema(
        summary="Обновление отзыва",
        description="Полное обновление отзыва по ID",
        request=ReviewSerializer,
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Отзыв"
            )
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление отзыва",
        description="Частичное обновление отзыва по ID",
        request=ReviewSerializer,
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Отзыв"
            )
        },
    ),
    destroy=extend_schema(
        summary="Удаление отзыва",
        description="Удаление отзыва по ID",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Отзыв удален"
            )
        },
    ),
)   
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()    
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    