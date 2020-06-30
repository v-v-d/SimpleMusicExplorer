from datetime import date

from django.db import models

from authapp.models import User


class FileModel(models.Model):
    file = models.FileField(blank=False, null=False, upload_to='images/albumart')

    def __str__(self):
        return self.file.name


class ArtistModel(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    location = models.CharField(max_length=128, blank=True)
    bio = models.CharField(max_length=512, blank=True)
    website = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


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
    artist = models.ForeignKey(ArtistModel, null=False, on_delete=models.CASCADE)
    cover = models.ManyToManyField(FileModel, blank=True)

    def __str__(self):
        return f'{self.title}'


class TrackModel(models.Model):
    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    artist = models.ForeignKey(ArtistModel, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False)
    album = models.ForeignKey('AlbumModel', related_name='tracks', null=False, on_delete=models.DO_NOTHING)
    order = models.SmallIntegerField()

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
