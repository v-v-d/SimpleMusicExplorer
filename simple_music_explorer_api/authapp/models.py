from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    is_artist = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'is_artist']

    def __str__(self):
        return self.username
