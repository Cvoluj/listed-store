from uuid import UUID
from django.conf import settings
from django.forms import ValidationError
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from store.product.models import Product
from .models import Cart


def get_cart(request: Request):
    cart_id = request.session.get(settings.SESSION_CART_KEY)
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = None
    else:
        cart = None

    if not cart:
        cart = Cart.objects.create(user=request.user)
        request.session[settings.SESSION_CART_KEY] = str(cart.id)
        request.session.set_expiry(180) 
    return cart

def get_product(public_id: UUID) -> Product:
    try:
        return Product.objects.get(public_id=public_id, hidden=False)
    except Product.DoesNotExist:
        raise NotFound(detail='Product not found')
    except ValidationError:
        raise NotFound(detail='Wrong public_id')
