from django.conf import settings
from rest_framework.request import Request

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