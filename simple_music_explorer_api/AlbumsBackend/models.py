from django.db import models
from django.utils import timezone


class AlbumModel(models.Model):
    db_table = 'albums'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_gte_0'),
        ]

    name = models.CharField(max_length=64, null=False)
    price = models.FloatField(default=0, null=False)
    genre = models.CharField(max_length=32)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=512)
    artist_name = models.CharField(max_length=128, null=False)
    artist_id = models.IntegerField(null=False)

    # TODO: add a cover art


class SongModel(models.Model):
    db_table = 'songs'

    name = models.CharField(max_length=64, null=False)
    artist_name = models.CharField(max_length=128, null=False)
    artist_id = models.IntegerField(null=False)
    album = models.ForeignKey('AlbumModel', related_name='tracks', null=False, on_delete=models.CASCADE)
    # album_id = models.ForeignKey('AlbumModel', null=False, on_delete=models.DO_NOTHING)
