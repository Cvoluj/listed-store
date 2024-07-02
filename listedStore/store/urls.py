from rest_framework_nested import routers


from store.cart.viewsets import CartViewSet
from store.user.viewsets import UserViewSet
from store.auth.viewsets import RefreshViewSet, RegisterViewSet, LoginViewSet
from store.product.viewsets import ProductViewSet

router = routers.SimpleRouter()

#USER
router.register(r'user', UserViewSet, basename='user')

#AUTH
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

#PRODUCT
router.register(r'product', ProductViewSet, basename='product')

    # path('cart/', CartView.as_view(), name='cart'),
    # path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    # path('cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),

#CART
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    *router.urls
]
