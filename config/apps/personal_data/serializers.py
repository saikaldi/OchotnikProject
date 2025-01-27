from rest_framework import serializers
from .models import UserProfile, UserAddress, UserPymentCard

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "user", "first_name", "last_name", "birth_date", "gender", "phone_number", "email","created_at", "updated_at"]
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ["id", "user", "country", "city", "district", "street", "house_number", "flat_number",  "created_at", "updated_at"]
        
    def update(self, instance, validated_data):
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.district = validated_data.get('district', instance.district)
        instance.street = validated_data.get('street', instance.street)
        instance.house_number = validated_data.get('house_number', instance.house_number)
        instance.flat_number = validated_data.get('flat_number', instance.flat_number)
        instance.save()
        return instance
        
class UserPymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPymentCard
        fields = ["id", "user", "card", "cardholder_name", "expiration_date", "cvv", "created_at", "updated_at"]
        
    def update(self, instance, validated_data):
        instance.card = validated_data.get('card', instance.card)
        instance.cardholder_name = validated_data.get('cardholder_name', instance.cardholder_name)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.cvv = validated_data.get('cvv', instance.cvv)
        instance.save()        
        return instance