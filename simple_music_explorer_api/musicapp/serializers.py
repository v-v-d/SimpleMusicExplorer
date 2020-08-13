from rest_framework import serializers

from authapp.serializers import UserSerializer
from musicapp.models import ArtistAlbum, AlbumTrack, FileModel, Artist


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ('id', 'file')


class TrackListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        tracks = [AlbumTrack(**item) for item in validated_data]
        return AlbumTrack.objects.bulk_create(tracks)


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=ArtistAlbum.objects.all())
    title = serializers.CharField(max_length=100, required=True)
    audio_file = serializers.SerializerMethodField()
    album_image = serializers.SerializerMethodField()

    class Meta:
        model = AlbumTrack
        fields = (
            'id', 'title', 'ordering', 'artist_name', 'album_title',
            'album_image', 'artist', 'album', 'audio_file'
        )
        list_serializer_class = TrackListSerializer

    def get_audio_file(self, track):
        request = self.context.get('request')
        audio_file_url = track.audio_file.first().file.url
        return request.build_absolute_uri(audio_file_url)

    def get_album_image(self, track):
        request = self.context.get('request')
        album_img_url = track.album_image.first().file.url
        return request.build_absolute_uri(album_img_url)


class AlbumSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    title = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = ArtistAlbum
        fields = ('id', 'artist_name', 'artist', 'title', 'price', 'genre', 'date', 'description', 'image')

    def get_image(self, album):
        request = self.context.get('request')
        image_url = album.image.first().file.url
        return request.build_absolute_uri(image_url)


class ArtistSerializer(serializers.ModelSerializer):
    """Сериализация артиста"""
    user = UserSerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ('id', 'user', 'name', 'location', 'bio', 'website', 'image')

    def get_image(self, artist):
        request = self.context.get('request')
        image_url = artist.image.first().file.url
        return request.build_absolute_uri(image_url)


class ArtistCreateSerializer(serializers.ModelSerializer):
    """Сериализация автиста"""

    class Meta:
        model = Artist
        fields = ('name', 'location', 'bio', 'website', 'logo')

    def create(self, validated_data):
        artist, _ = Artist.objects.update_or_create(**validated_data)
        return artist
