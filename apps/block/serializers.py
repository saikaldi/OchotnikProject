from rest_framework import serializers
from .models import Block, AboutUs

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'title', 'text', 'photo',  'created_at']
        
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'name', 'test', 'photo', 'created_at']