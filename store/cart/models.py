from django.db import models
from django.conf import settings
from rest_framework.exceptions import NotFound

from store.abstract.models import AbstractModel, AbstractManager


class Cart(AbstractModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def retrieve_product_from_cart(self, product):
        try:      
            cart_item = self.items.get(product=product)
            return cart_item
        except CartItem.DoesNotExist:
            raise NotFound(detail='Item not found in your cart')
    
    def remove_product(self, product):
        self.retrieve_product_from_cart(product).delete()
        
    def __str__(self):
        return f"Cart {self.id} for {self.user}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('store_product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AbstractManager()
