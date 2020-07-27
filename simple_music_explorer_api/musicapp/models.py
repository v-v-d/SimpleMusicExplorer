from django.db import models

from authapp.models import User
from coreapp.models import Core


class FileModel(models.Model):
    file = models.FileField(blank=False, null=False, upload_to='images')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name


class ArtistModel(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    location = models.CharField(max_length=128, blank=True)
    bio = models.CharField(max_length=512, blank=True)
    website = models.CharField(max_length=32, blank=True)
    logo = models.ManyToManyField(FileModel, blank=True)

    def __str__(self):
        return self.name


class AlbumModel(Core):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_gte_0'),
        ]

    price = models.FloatField(default=0, null=False)
    genre = models.CharField(max_length=32)
    artist = models.ForeignKey(ArtistModel, null=True, on_delete=models.CASCADE)
    cover = models.ManyToManyField(FileModel, blank=True)

    def __str__(self):
        return f'{self.title}'


class TrackModel(Core):
    class Meta:
        ordering = ['order']

    artist = models.ForeignKey(ArtistModel, null=False, on_delete=models.CASCADE)
    album = models.ForeignKey('AlbumModel', related_name='tracks', null=False, on_delete=models.DO_NOTHING)
    audio_file = models.FileField(upload_to='audio')
    order = models.SmallIntegerField()

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
