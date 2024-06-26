
from store.abstract.serializers import AbstractSerializer
from store.user.models import User


class UserSerializer(AbstractSerializer):
    class Meta:
        model = User
        fields = ['public_id', 'username', 'first_name', 'last_name',
                  'email', 'is_active', 'created', 'updated']
        read_only_fields = ['is_active']