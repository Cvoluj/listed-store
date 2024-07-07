from rest_framework.permissions import IsAuthenticated

from store.abstract.viewsets import AbstractViewSet
from store.user.serializers import UserSerializer
from store.user.models import User


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['public_id'])
        self.check_object_permissions(self.request, obj)

        return obj
