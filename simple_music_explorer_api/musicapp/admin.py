from django.contrib import admin

from .models import AlbumModel, TrackModel, FileModel, ArtistModel

admin.site.register(ArtistModel)
admin.site.register(AlbumModel)
admin.site.register(TrackModel)
admin.site.register(FileModel)
