from django.db import models

from coreapp.models import Core
from musicapp.models import ArtistModel
from orderapp.models import OrderItem


class BillingInformation(Core):
    seller = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    grant_type = models.CharField(max_length=100)


class Refund(models.Model):
    order = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"

