from django.db import models

from authapp.models import User
from coreapp.models import Core, FileModel


class Artist(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    location = models.CharField(max_length=128, blank=True)
    bio = models.CharField(max_length=512, blank=True)
    website = models.CharField(max_length=32, blank=True)
    image = models.ManyToManyField(FileModel, blank=True)

    def __str__(self):
        return self.name


class ArtistAlbum(Core):
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_gte_0'),
        ]

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=False)
    genre = models.CharField(max_length=32)
    artist = models.ForeignKey(Artist, blank=False, null=False, on_delete=models.CASCADE)
    image = models.ManyToManyField(FileModel, blank=True)

    @property
    def artist_name(self):
        return self.artist.name

    def __str__(self):
        return f'{self.title}'


class AlbumTrack(Core):
    class Meta:
        ordering = ['ordering']

    artist = models.ForeignKey(Artist, null=False, on_delete=models.CASCADE)
    album = models.ForeignKey(ArtistAlbum, related_name='tracks', null=False, on_delete=models.DO_NOTHING)
    audio_file = models.ManyToManyField(FileModel, blank=False)
    duration = models.FloatField(default=0)
    ordering = models.PositiveSmallIntegerField()

    @property
    def artist_name(self):
        return self.artist.name

    @property
    def album_title(self):
        return self.album.title

    @property
    def album_image(self):
        return self.album.image

    def __str__(self):
        return f'{self.ordering}: {self.title}'
