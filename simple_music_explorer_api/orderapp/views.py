from pprint import pprint

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orderapp.models import Address
from orderapp.serializers import AddressSerializer, AddressCreateSerializer


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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):
    pass


class OrderUpdateView(APIView):
    pass