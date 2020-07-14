from rest_framework import serializers

from authapp.serializers import UserSerializer
from musicapp.serializers import ArtistSerializer
from .models import OrderItem, Address


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('artist', 'merch_product', 'album_product', 'price', 'quantity', 'order')


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Address
        # fields = ('id', 'user', 'first_name', 'last_name', 'email', 'street_address', 'apartment_address', 'zip', 'city', 'default')
        fields = '__all__'

class AddressCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'email', 'street_address', 'apartment_address', 'zip', 'city', 'default')

    def create(self, validated_data):
        address, _ = Address.objects.update_or_create(**validated_data)
        return address
