from rest_framework import serializers, permissions
from albumapp.models import AlbumModel, TrackModel, FileModel


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ('id', 'file')


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all())

    class Meta:
        model = TrackModel
        fields = ('id', 'title', 'order', 'artist', 'album')


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    cover = serializers.HyperlinkedRelatedField()

    class Meta:
        model = AlbumModel
        fields = ('id', 'artist', 'title', 'price', 'genre', 'date', 'description', 'tracks', 'cover')
