from rest_framework import serializers, permissions
from albumapp.models import AlbumModel, TrackModel


class TrackSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticated, ]

    album = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all())

    class Meta:
        model = TrackModel
        fields = ('id', 'title', 'order', 'artist', 'album')


class AlbumSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticated, ]

    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = AlbumModel
        fields = ('id', 'artist', 'title', 'price', 'genre', 'date', 'description', 'tracks')
