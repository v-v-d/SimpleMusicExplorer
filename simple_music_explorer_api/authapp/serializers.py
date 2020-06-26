from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password')
