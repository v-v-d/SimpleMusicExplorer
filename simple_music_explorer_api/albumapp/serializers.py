from rest_framework import serializers, permissions
from albumapp.models import AlbumModel, TrackModel, FileModel


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ('id', 'file')


class TrackListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        tracks = [TrackModel(**item) for item in validated_data]
        return TrackModel.objects.bulk_create(tracks)


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all())

    class Meta:
        model = TrackModel
        fields = ('id', 'title', 'order', 'artist', 'album')
        list_serializer_class = TrackListSerializer


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    cover = serializers.StringRelatedField(many=True)

    class Meta:
        model = AlbumModel
        fields = ('id', 'artist', 'title', 'price', 'genre', 'date', 'description', 'tracks', 'cover')
