from rest_framework import serializers

from authapp.serializers import UserSerializer
from merchapp.serializers import ProductSerializer
from musicapp.serializers import ArtistSerializer, AlbumSerializer
from .models import OrderItem, Address, Orders, ProductOrAlbumToOrder, PurchasedTrack


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


class PurchasedTrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=ProductOrAlbumToOrder.objects.all())

    class Meta:
        model = PurchasedTrack
        fields = ('id', 'title', 'album', 'order', 'audio_file')


class ProductOrAlbumToOrderSerializer(serializers.ModelSerializer):
    prod_tracks = PurchasedTrackSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOrAlbumToOrder
        fields = ('id', 'title', 'artist', 'category', 'prod_tracks')


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
    fixed_product = ProductOrAlbumToOrderSerializer()
    merch = ProductSerializer()
    album = AlbumSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'merch', 'album', 'fixed_product', 'price', 'quantity', 'delivery_status')


class OrderSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = ('id', 'total_sum', 'artist', 'owner', 'delivery_address', 'payment_state', 'order_items')
