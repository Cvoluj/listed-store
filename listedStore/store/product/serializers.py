from rest_framework import serializers
from .models import Product
from store.abstract.serializers import AbstractSerializer

class ProductSerializer(AbstractSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_public_id = serializers.ReadOnlyField(source='user.public_id')
    
    class Meta:
        model = Product
        fields = ['public_id', 'name', 'description', 'price', 'stock', 'user', 'user_public_id', 'hidden', 'created', 'updated']
