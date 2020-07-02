from django.db import models
from authapp.models import User


class BasketModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
