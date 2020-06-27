from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    is_artist = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['is_artist']

    def __str__(self):
        return self.username


class Artist(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    location = models.CharField(max_length=128, blank=True)
    bio = models.CharField(max_length=512, blank=True)
    website = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name

