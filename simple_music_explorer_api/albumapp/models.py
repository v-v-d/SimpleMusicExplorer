from datetime import date

from django.db import models
from authapp.models import Artist


class AlbumModel(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_gte_0'),
        ]

    title = models.CharField(max_length=64, null=False)
    price = models.FloatField(default=0, null=False)
    genre = models.CharField(max_length=32)
    date = models.DateField(default=date.today)
    description = models.CharField(max_length=512)
    artist = models.ForeignKey('Artist', null=False, on_delete=models.CASCADE)

    # TODO: add a cover art


class TrackModel(models.Model):
    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    artist = models.ForeignKey('Artist', null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False)
    album = models.ForeignKey('AlbumModel', related_name='tracks', null=False, on_delete=models.DO_NOTHING)
    order = models.IntegerField()

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
