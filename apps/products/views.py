from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, Cart, FavoriteProduct, Review
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, FavoriteProductSerializer, ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
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
                
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()   
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

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
   
class FavoriteProductViewSet(viewsets.ModelViewSet):
    queryset = FavoriteProduct.objects.all()    
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        favorite_products = FavoriteProduct.objects.all()
        favorite_products_serializer = FavoriteProductSerializer(favorite_products, many=True)
        products_serializer = ProductSerializer([favorite_product.product_id for favorite_product in favorite_products], many=True)
        for favorite_product, product in zip(favorite_products_serializer.data, products_serializer.data):
            favorite_product['product'] = product
        return Response({"favorite_products": favorite_products_serializer.data})
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        favorite_product = get_object_or_404(FavoriteProduct, pk=pk)
        favorite_product_serializer = FavoriteProductSerializer(favorite_product)
        product_serializer = ProductSerializer(favorite_product.product_id)
        return Response({"favorite_product": favorite_product_serializer.data, "product": product_serializer.data})
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()    
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    