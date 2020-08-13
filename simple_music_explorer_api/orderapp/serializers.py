from rest_framework import serializers

from authapp.serializers import UserSerializer
from merchapp.serializers import ProductSerializer
from musicapp.serializers import ArtistSerializer, AlbumSerializer, FileSerializer
from .models import OrderItem, Address, UserOrder, FrozenOrderItem, FrozenTrack


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
    album = serializers.PrimaryKeyRelatedField(queryset=FrozenOrderItem.objects.all())

    class Meta:
        model = FrozenTrack
        fields = ('id', 'title', 'album', 'order', 'audio_file')


class ProductOrAlbumToOrderSerializer(serializers.ModelSerializer):
    prod_tracks = PurchasedTrackSerializer(many=True, read_only=True)
    image = FileSerializer(many=True)

    class Meta:
        model = FrozenOrderItem
        fields = ('id', 'title', 'artist', 'category', 'image', 'short_desc', 'prod_tracks')


class OrderOwnerSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = UserOrder
        fields = ('owner', )


class OrderItemSerializer(serializers.ModelSerializer):
    # order = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
    order = OrderOwnerSerializer()
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
        model = UserOrder
        fields = ('id', 'total_sum', 'artist', 'owner', 'delivery_address', 'payment_state', 'order_items')
