# from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")
