from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from basketapp.models import BasketModel
from musicapp.models import TrackModel
from orderapp.models import Address, Orders, ProductOrAlbumToOrder, OrderItem, PurchasedTrack
from orderapp.serializers import AddressSerializer, AddressCreateSerializer, ProductOrAlbumToOrderSerializer, \
    OrderItemSerializer, OrderSerializer


def create_orders(request, address_id):
    owner = request.user
    basket = BasketModel.objects.filter(owner=owner)
    order_list = list()
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
            tracks = TrackModel.objects.filter(album=obj)
            prod_album = obj
            artist_name = item.album.artist.name

        serializer = ProductOrAlbumToOrderSerializer([obj], many=True)
        prod_fields = serializer.data[0]
        prod_fields.pop('id')
        if artist_name:
            prod_fields['artist'] = artist_name

        fixed_product = ProductOrAlbumToOrder.objects.create(**prod_fields)

        if tracks:
            for track in tracks:
                PurchasedTrack.objects.create(album=fixed_product,
                                              audio_file=track.audio_file.url,
                                              order=track.order)

        order, _ = Orders.objects.get_or_create(artist=artist,
                                                owner=owner,
                                                payment_state='NP',
                                                delivery_address=address)

        order.total_sum = order.total_sum + float(price * quantity)
        order.save()

        if order not in order_list:
            order_list.append(order)
        order_item_dict = model_to_dict(item)
        order_item_dict['order'] = order
        order_item_dict['fixed_product'] = fixed_product
        order_item_dict['merch'] = prod_merch
        order_item_dict['album'] = prod_album

        order_item_serializer = OrderItemSerializer([order_item_dict], many=True)
        order_item = order_item_serializer.data[0]
        order_item.pop('id')
        order_item['order'] = order
        order_item['fixed_product'] = fixed_product
        order_item['merch'] = prod_merch
        order_item['album'] = prod_album
        OrderItem.objects.create(**order_item)

    basket.delete()


class NeedAnAddress(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        basket = BasketModel.objects.filter(owner=request.user)
        need_an_address = False
        for item in basket:
            if item.merch:
                need_an_address = True
        return Response(data={'need_an_address': need_an_address})


class AddressView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):

        address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

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
        orders = Orders.objects.filter(owner=request.user, payment_state='NP')
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request):

        address_id = request.data.get('address_id')
        create_orders(request, address_id)
        orders = Orders.objects.filter(owner=request.user, payment_state='NP')
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



