from uuid import UUID
from django.forms import ValidationError
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotFound

from store.product.models import Product
from .models import CartItem
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer
from .service import get_cart

class CartViewSet(GenericViewSet, 
                  mixins.CreateModelMixin, 
                #   mixins.DestroyModelMixin
            ):
    permission_classes = [IsAuthenticated]
    lookup_field = 'public_id'
    
    def list(self, request: Request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        request.session.set_expiry(180)

        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_cart(request)
        product = serializer.validated_data['concrete_product']
        
        quantity = request.data.get('quantity', 1)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        
        request.session.set_expiry(180)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request: Request, public_id: UUID):
        cart = get_cart(request)
        
        try:
            product = Product.objects.get(public_id=public_id, hidden=False)
        except Product.DoesNotExist:
            raise NotFound(detail='Product not found')
        except ValidationError:
            raise NotFound(detail='Wrong public_id')
        
        cart.remove_product(product)  

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)    

    # @action(detail=False, methods=['post'])
    # def clear(self, request: Request):
    #     cart = get_cart(request)
    #     product_id = request.data.get('product')
    #     product = get_object_or_404(Product, pk=product_id)
    #     cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    #     cart_item.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def remove(self):
    #     ...
    
    def get_serializer_class(self):
        if self.action in ["create"]:
            return AddCartItemSerializer

        return super().get_serializer_class()