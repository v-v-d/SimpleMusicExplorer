from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from basketapp.models import BasketModel
from basketapp.serializers import BasketSerializer, BasketCreateSerializer


class BasketViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = BasketModel.objects.all()
    serializer_class = BasketSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class BasketChangeItem(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def put(self, request, pk):
        basket_update = BasketModel.objects.filter(id=pk)
        serialize = BasketCreateSerializer(data=request.data)
        if serialize.is_valid():
            basket_update.update(**serialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        artist_delete = BasketModel.objects.filter(id=pk)
        artist_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
