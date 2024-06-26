from uuid import UUID
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework import pagination, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from store.product.serializers import ProductSerializer
from store.product.models import Product
from store.abstract.viewsets import AbstractViewSet
from store.user.models import User


class ProductPagination(pagination.PageNumberPagination):
    page_size = 20


class ProductViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put')
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'public_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.exclude(hidden=True)

    def get_object(self):
        obj = Product.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)

        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        product = Product.objects.create(
            user=request.user,
            **serializer.validated_data
        )
        
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    
    def update(self, request: Request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        public_id = kwargs.get('public_id')
        product = Product.objects.get(public_id=public_id)
        
        if request.user != product.user:
            return Response({"detail": "You do not have permission to update this product."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
        
    @action(methods=['PUT'],  detail=True)
    def hide(self, request, public_id: UUID | None, *args, **kwargs):        
        if not public_id:
            return Response({"detail": "Public key is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        product: Product = Product.objects.get_object_by_public_id(public_id)
        
        if product.hidden is True:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != product.user:
            return Response({"detail": "You do not have permission to hide this product."}, status=status.HTTP_401_UNAUTHORIZED)
        
        product.hidden = True
        product.save()
        return Response({"detail": "Product has been hidden."}, status=status.HTTP_202_ACCEPTED)
        
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])    
    def get_own_products(self, request: Request, *args, **kwargs):        
        products: list[Product] | Product | None = Product.objects.filter(user=request.user, hidden=False)
        
        if products is None:
            return Response({"detail": "You do not published any posts yet"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path='by_user/(?P<user_public_id>[^/.]+)')
    def get_by_user(self, request, user_public_id=None, *args, **kwargs):
        try:
            user = User.objects.get(public_id=user_public_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if self.request.user.is_superuser:
            products = Product.objects.filter(user=user)
        products = Product.objects.filter(user=user, hidden=False)        
        
        if not products.exists():
            return Response({"detail": "This user has not published any products yet."}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        