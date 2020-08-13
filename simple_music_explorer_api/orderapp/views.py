from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from basketapp.models import BasketModel
from musicapp.models import AlbumTrack
from orderapp.models import Address, UserOrder, FrozenOrderItem, OrderItem, FrozenTrack
from orderapp.serializers import AddressSerializer, AddressCreateSerializer, ProductOrAlbumToOrderSerializer, \
    OrderItemSerializer, OrderSerializer


def create_orders(request, address_id=None):
    owner = request.user
    basket = BasketModel.objects.filter(owner=owner)
    order_list = []
    address = None
    if address_id:
        address = get_object_or_404(Address, id=address_id)

    for item in basket:
        prod_merch = None
        prod_album = None

        price = item.price
        quantity = item.quantity
        artist_name = None
        tracks = None
        if item.type_product == 'm':
            artist = item.merch.artist
            obj = item.merch
            prod_merch = obj
        else:
            artist = item.album.artist
            obj = item.album
            tracks = AlbumTrack.objects.filter(album=obj)
            prod_album = obj
            artist_name = item.album.artist.name

        prod_fields = dict()
        if artist_name:
            prod_fields['artist'] = artist_name
            prod_fields['genre'] = obj.genre
        else:
            prod_fields['category'] = obj.category.title
            prod_fields['short_desc'] = obj.short_desc
        prod_fields['title'] = obj.title
        fixed_product = FrozenOrderItem.objects.create(**prod_fields)
        if not artist_name:
            fixed_product.image.set(obj.image.all())

        if tracks:
            for track in tracks:
                FrozenTrack.objects.create(album=fixed_product,
                                           title=track.title,
                                           audio_file=track.audio_file.url,
                                           order=track.ordering)

        order, _ = UserOrder.objects.get_or_create(artist=artist,
                                                   owner=owner,
                                                   payment_state='NP',
                                                   delivery_address=address)
        order.total_sum = order.total_sum + float(price * quantity)
        order.save()

        if order not in order_list:
            order_list.append(order)

        order_item_dict = dict()
        order_item_dict['order'] = order
        order_item_dict['fixed_product'] = fixed_product
        order_item_dict['merch'] = prod_merch
        order_item_dict['album'] = prod_album
        order_item_dict['type_product'] = item.type_product
        order_item_dict['price'] = price
        order_item_dict['quantity'] = quantity
        OrderItem.objects.create(**order_item_dict)

    basket.delete()


class AddressView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        basket = BasketModel.objects.filter(owner=request.user)
        need_an_address = False
        for item in basket:
            if item.merch:
                need_an_address = True
        if need_an_address:
            address = Address.objects.filter(user=request.user)
            serializer = AddressSerializer(address, many=True)
            return Response(data={'address': serializer.data})
        return Response(data={'need_an_address': need_an_address})

    def post(self, request):

        serializer = AddressCreateSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.save(user=request.user)
            serializer = AddressSerializer([address], many=True)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class InvoiceForPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        orders = UserOrder.objects.filter(owner=request.user, payment_state='NP')
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request):

        address_id = request.data.get('address_id')
        create_orders(request, address_id)
        orders = UserOrder.objects.filter(owner=request.user, payment_state='NP')
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



