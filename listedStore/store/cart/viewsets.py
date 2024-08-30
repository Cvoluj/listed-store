from uuid import UUID
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from .models import CartItem
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, PutCartItemSerializer
from .service import get_cart, get_product, update_session_expiry
from store.user.models import User
from store.rmq.service import RMQReceiptProducer
from store.rmq.message import MessageItem
from store.smtp_mail.models import SMTPMail


class CartViewSet(GenericViewSet, 
                  mixins.CreateModelMixin, 
            ):
    permission_classes = [IsAuthenticated]
    lookup_field = 'public_id'
    
    @update_session_expiry(180)
    def list(self, request: Request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @update_session_expiry(180)
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
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @update_session_expiry(180)
    @action(detail=True, methods=['post'])
    def remove_item(self, request: Request, public_id: UUID):
        cart = get_cart(request)
        cart.remove_product(get_product(public_id))  
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)   
    
    @update_session_expiry(180)
    @action(detail=False, methods=['put'], serializer_class=PutCartItemSerializer)
    def change_quantity(self, request: Request):
        cart = get_cart(request)
        serializer = PutCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_product(serializer.validated_data['product'])
        cart_item: CartItem = cart.retrieve_product_from_cart(product)
        
        updated_quantity = cart_item.quantity + serializer.validated_data['quantity']
        if updated_quantity <= 0:
            cart.remove_product(product)
            cart.save()
        else:
            cart_item.quantity = updated_quantity
            cart_item.save()
        
        return Response(CartSerializer(cart).data)
        
    @update_session_expiry(180)    
    @action(detail=False, methods=['delete'])
    def clear(self, request: Request):
        cart = get_cart(request)
        cart.get_all_products().delete()
        return Response(CartSerializer(cart).data)
    
    
    def get_serializer_class(self):
        if self.action in ["create"]:
            return AddCartItemSerializer

        return super().get_serializer_class()
    
    @update_session_expiry(180)
    @action(detail=False, methods=['post'])
    def buy(self, request: Request):
        cart = get_cart(request)
        user: User = request.user
        items: list[CartItem] = list(cart.get_all_products())

        message_items = [
            MessageItem(
                name=item.product.name, 
                quantity=item.quantity, 
                price=item.product.price
            ) for item in items    
        ]

        smtp_mail = SMTPMail.objects.get(name='listedStore')

        rmq_producer = RMQReceiptProducer(smtp_mail=smtp_mail)
        rmq_producer.send_receipt_message(email_reciever=user.email, message_items=message_items)


        cart.get_all_products().delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK) 
        