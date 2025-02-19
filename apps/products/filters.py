import django_filters
from .models import Category, Product, Cart, FavoriteProduct, Review

class CategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name='category_name', lookup_expr='icontains')
    
    class Meta:
        model = Category
        fields = ['category_name']

class ProductFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains')            # Поиск по названию товара
    price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')                               # Поиск по цене
    is_new = django_filters.BooleanFilter(field_name='is_new', lookup_expr='isnull')                        # Поиск по новости
    is_hot = django_filters.BooleanFilter(field_name='is_hot', lookup_expr='isnull')                        # Поиск по горячим товарам
    is_special = django_filters.BooleanFilter(field_name='is_special', lookup_expr='isnull')                 # Поиск по специальным товарам
    is_promo = django_filters.BooleanFilter(field_name='is_promo', lookup_expr='isnull')                    # Поиск по промо товарам
    is_discount = django_filters.BooleanFilter(field_name='is_discount', lookup_expr='isnull')              # Поиск по скидкам
    
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'is_new', 'is_hot', 'is_special', 'is_promo', 'is_discount',]

class CartFilter(django_filters.FilterSet):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'total_price']

class FavoriteProductFilter(django_filters.FilterSet):
    class Meta:
        model = FavoriteProduct
        fields = ['user', 'product_id']

class ReviewFilter(django_filters.FilterSet):
    class Meta:
        model = Review        
        fields = ['user', 'product_id', 'rating']