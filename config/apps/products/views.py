from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

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
        return Response({"product": product_serializer.data, "reviews": review_serializer.data})    
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()   
    serializer_class = CartSerializer
    
    def list(self, request, *args, **kwargs):
        carts = Cart.objects.all()
        carts_serializer = CartSerializer(carts, many=True)
        products_serializer = ProductSerializer([cart.product for cart in carts], many=True)
        for cart, product in zip(carts_serializer.data, products_serializer.data):
            cart['product'] = product
        cart_total_price = sum([cart.cart_total_price() for cart in carts])
        return Response({"carts": carts_serializer.data, "cart_total_price": cart_total_price})
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=pk)
        cart_serializer = CartSerializer(cart)
        product_serializer = ProductSerializer(cart.product)
        return Response({"cart": cart_serializer.data, "product": product_serializer.data})
   
class FavoriteProductViewSet(viewsets.ModelViewSet):
    queryset = FavoriteProduct.objects.all()    
    serializer_class = FavoriteProductSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()    
    serializer_class = ReviewSerializer
    