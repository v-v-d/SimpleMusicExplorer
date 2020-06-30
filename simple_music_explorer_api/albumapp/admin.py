from django.contrib import admin

from .models import AlbumModel, TrackModel, FileModel

admin.site.register(AlbumModel)
admin.site.register(TrackModel)
admin.site.register(FileModel)
