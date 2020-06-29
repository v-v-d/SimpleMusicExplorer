# from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from .models import User, Artist


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")


class ArtistSerializer(serializers.ModelSerializer):
    """Сериализация автиста"""
    user = UserSerializer()

    class Meta:
        model = Artist
        fields = ('id', 'user', 'name', 'location', 'bio', 'website')


class ArtistCreateSerializer(serializers.ModelSerializer):
    """Сериализация автиста"""

    class Meta:
        model = Artist
        fields = ('name', 'location', 'bio', 'website')

    def create(self, validated_data):
        artist = Artist.objects.update_or_create(**validated_data)
        return artist




# class UserCreateSerializer(BaseUserRegistrationSerializer):
#
#     class Meta(BaseUserRegistrationSerializer.Meta):
#         model = User
#         fields = ('id', 'first_name')
#
#
# class UserUpdateSerializer(UserSerializer):
#
#     class Meta(UserSerializer.Meta):
#         model = User
#         fields = ('id', 'first_name')
#         read_only_fields = ('email',)


