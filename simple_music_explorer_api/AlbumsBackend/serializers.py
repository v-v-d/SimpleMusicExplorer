from rest_framework import serializers
from AlbumsBackend.models import AlbumModel, TrackModel


class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = AlbumModel
        fields = ('id', 'name', 'price', 'genre', 'date', 'description', 'artist_name', 'artist_id', 'tracks')

    def create(self, validated_data):
        """
        Create and return new Album instance, given valid data
        """
        return AlbumModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.artist_name = validated_data.get('artist_name', instance.artist_name)
        instance.artist_id = validated_data.get('artist_id', instance.artist_id)
        instance.save()
        return instance


class TrackSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=AlbumModel.objects.all())

    class Meta:
        model = TrackModel
        fields = ('id', 'name', 'artist_id', 'artist_name', 'album')
