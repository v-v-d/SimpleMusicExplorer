from datetime import date

from django.db import models


class AlbumModel(models.Model):
    class Meta:
        db_table = 'albums'
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_gte_0'),
        ]

    title = models.CharField(max_length=64, null=False)
    price = models.FloatField(default=0, null=False)
    genre = models.CharField(max_length=32)
    date = models.DateField(default=date.today)
    description = models.CharField(max_length=512)
    artist_name = models.CharField(max_length=128, null=False)
    artist_id = models.IntegerField(null=False)

    # TODO: add a cover art


class TrackModel(models.Model):
    class Meta:
        db_table = 'tracks'
        unique_together = ['album', 'order']
        ordering = ['order']

    artist_name = models.CharField(max_length=128, null=False)
    artist_id = models.IntegerField(null=False)
    title = models.CharField(max_length=64, null=False)
    album = models.ForeignKey('AlbumModel', related_name='tracks', null=False, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
