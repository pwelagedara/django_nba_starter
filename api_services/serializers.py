from rest_framework import serializers
from drf_enum_field.serializers import EnumFieldSerializerMixin

from api_services import models


class UserInfoSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    """Serializes a User object"""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'role')




