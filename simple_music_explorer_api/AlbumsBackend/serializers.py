from rest_framework import serializers
from AlbumsBackend.models import AlbumModel, TrackModel


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all())

    class Meta:
        model = TrackModel
        fields = ('id', 'title', 'order', 'artist_id', 'artist_name', 'album')


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = AlbumModel
        fields = ('id', 'title', 'price', 'genre', 'date', 'description', 'artist_name', 'artist_id', 'tracks')
