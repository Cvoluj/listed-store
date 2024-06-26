from typing import Dict, Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from store.user.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """
    Login serializer for requests and user creation
    """
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        
        refresh = self.get_token(self.user)
        
        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
