from rest_framework import serializers
from .models import Category, Product, Cart, FavoriteProduct

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ "id", "category_name", "created_at"]
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ["id",  "category", "product_name", "country", "brand", "model", "color", "size", "material", "price", "description", "image", "quantity", "is_new", "is_hot", "is_special", "is_promo",  "is_discount", "discount_percent", "discount_price", "created_at", ]
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "user", "product", "quantity", 'total_price', "created_at"]
    
    def validate(self, data):
        if Cart.objects.filter(user=data['user'], product=data['product']).exists():
            raise serializers.ValidationError("Товар уже в корзине")
        return data   
        
class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product_id", "created_at"] 
        
    def validate(self, data):
        if FavoriteProduct.objects.filter(user=data['user'], product_id=data['product_id']).exists():
            raise serializers.ValidationError("Товар уже в избранном")        
        return data
        