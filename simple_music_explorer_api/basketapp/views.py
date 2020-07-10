from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from basketapp.models import BasketModel
from basketapp.permissions import IsOwnerOnly
from basketapp.serializers import BasketSerializer


class BasketViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOnly)
    queryset = BasketModel.objects.all()
    serializer_class = BasketSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
