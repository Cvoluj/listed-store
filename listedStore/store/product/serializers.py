from rest_framework import serializers
from .models import Product
from store.abstract.serializers import AbstractSerializer

class ProductSerializer(AbstractSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Product
        fields = ['public_id', 'name', 'description', 'price', 'stock', 'user', 'hidden', 'created', 'updated']
