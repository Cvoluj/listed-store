from django.shortcuts import get_object_or_404
from rest_framework import serializers

from store.product.models import Product
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    public_id = serializers.ReadOnlyField(source='product.public_id')
    
    class Meta:
        model = CartItem
        fields = ['public_id', 'name', 'quantity', 'created', 'updated']

    def get_name(self, obj):
        return obj.product.name
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user_public_id = serializers.ReadOnlyField(source='user.public_id')
    
    class Meta:
        model = Cart
        fields = ['public_id', 'user_public_id', 'items', 'created', 'updated']
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField()
    quantity = serializers.IntegerField(default=1)
    
    class Meta:
        model=CartItem
        fields=['product', 'quantity']
    
    def validate_quantity(self, value):
        """
        Check that the quantity is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
    
    def validate(self, data):
        """
        This validation additionally adds `concrete_product` key with Product object
        """
        self.validate_quantity(data.get('quantity', 1))         
    
        concrete_product = get_object_or_404(Product, public_id=data.get('product'), hidden=False) 
        data['concrete_product'] = concrete_product  
        
        return data
    