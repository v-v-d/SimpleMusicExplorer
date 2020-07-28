from rest_framework import serializers

from authapp.serializers import UserSerializer
from musicapp.models import AlbumModel, TrackModel, FileModel, ArtistModel


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
    title = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = TrackModel
        fields = ('id', 'title', 'order', 'artist', 'album', 'audio_file')
        list_serializer_class = TrackListSerializer


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    cover = serializers.StringRelatedField(many=True)
    title = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = AlbumModel
        fields = ('id', 'artist', 'title', 'price', 'genre', 'date', 'description', 'tracks', 'cover')


class ArtistSerializer(serializers.ModelSerializer):
    """Сериализация артиста"""
    user = UserSerializer()

    class Meta:
        model = ArtistModel
        fields = ('id', 'user', 'name', 'location', 'bio', 'website', 'logo')


class ArtistCreateSerializer(serializers.ModelSerializer):
    """Сериализация автиста"""
    logo = serializers.PrimaryKeyRelatedField(queryset=FileModel.objects.all(), write_only=True, many=True,
                                              required=False)

    class Meta:
        model = ArtistModel
        fields = ('name', 'location', 'bio', 'website', 'logo')

    def update(self, instance, validated_data):
        logo = validated_data.pop('logo', None)
        instance = super().update(instance, validated_data)

        if logo is not None:
            for logo in logo:
                instance.logo.add(logo)
            instance.save()

        return instance

    def create(self, validated_data):
        artist, _ = ArtistModel.objects.update_or_create(**validated_data)
        return artist
