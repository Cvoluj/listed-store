from datetime import datetime
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from drf_spectacular.utils import extend_schema

from store.user.models import User
from store.auth.serializers import LoginSerializer


@extend_schema(
    request=LoginSerializer,
    responses={200: LoginSerializer}
)
class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )
    http_method_names = ('post')

    def create(self, request, *args, **kwargs):
        serializer: LoginSerializer = self.serializer_class(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        
        user: User = User.objects.get(email=serializer.validated_data['user']['email'])
        user.last_login = datetime.utcnow()
        user.save(update_fields=['last_login'])
        
        return Response(serializer.validated_data, status.HTTP_200_OK)
