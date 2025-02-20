import django_filters
from .models import Product, Category, Cart, FavoriteProduct, Review

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    model = django_filters.CharFilter(lookup_expr='icontains')
    brand = django_filters.CharFilter(lookup_expr='icontains')
    size = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'price__gt', 'price__lt', 'model', 'brand', 'size', 'color']
        
class CategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Category
        fields = ['category_name']
        
class CartFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(lookup_expr='icontains')
    product = django_filters.CharFilter(lookup_expr='icontains')
    quantity = django_filters.NumberFilter()
    total_price = django_filters.NumberFilter()
    
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity', 'total_price']
        
class FavoriteProductFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(lookup_expr='icontains')
    product_id = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = FavoriteProduct
        fields = ['user', 'product_id']
        
class ReviewFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(lookup_expr='icontains')
    product_id = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Review
        fields = ['user', 'product_id']
    