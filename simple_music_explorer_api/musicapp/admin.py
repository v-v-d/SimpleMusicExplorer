from django.contrib import admin

from .models import ArtistAlbum, AlbumTrack, FileModel, Artist

admin.site.register(Artist)
admin.site.register(ArtistAlbum)
admin.site.register(AlbumTrack)
admin.site.register(FileModel)
