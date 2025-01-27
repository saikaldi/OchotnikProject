from rest_framework import serializers
from .models import Category, Product, Cart, FavoriteProduct, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ "id", "category_name", "created_at"]
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            "id","category", "product_name", "country", "brand", 
            "model", "color", "size", "material", "price", "description", 
            "image", "quantity", "is_new", "is_hot", "is_special", "is_promo", 
            "is_discount", "discount_percent", "discount_price", "created_at",
            ]
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "user", "product", "quantity", 'total_price', "created_at"]
    
    def validate(self, data):
        if 'user' in data and 'product' in data:
            if Cart.objects.filter(user=data['user'], product=data['product']).exists():
                cart = Cart.objects.get(user=data['user'], product=data['product'])
                if 'quantity' in data:
                    cart.quantity = data['quantity']
                if 'total_price' in data:
                    cart.total_price = data['total_price']
                cart.save()
                return {'id': cart.id, 'user': cart.user, 'product': cart.product, 'quantity': cart.quantity, 'total_price': cart.total_price}
        return data
    
    def update(self, instance, validated_data):
        if 'user' in validated_data and 'product' in validated_data:
            if Cart.objects.filter(user=validated_data['user'], product=validated_data['product']).exists():
                if instance.user != validated_data['user'] or instance.product != validated_data['product']:
                    raise serializers.ValidationError("Товар уже в корзине")
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()
        return instance
    
class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product_id", "created_at"] 
        
    def validate(self, data):
        if FavoriteProduct.objects.filter(user=data['user'], product_id=data['product_id']).exists():
            raise serializers.ValidationError("Товар уже в избранном")        
        return data
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "product_id", "text", "rating", "photo", "created_at"]