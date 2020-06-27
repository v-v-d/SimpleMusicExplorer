from rest_framework import serializers
from AlbumsBackend.models import AlbumModel


class AlbumSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=64)
    price = serializers.FloatField(min_value=0, required=True)
    genre = serializers.CharField(max_length=32)
    date = serializers.DateField(required=True)
    description = serializers.CharField(max_length=512, allow_blank=True)
    artist_name = serializers.CharField(max_length=128, allow_blank=False)
    artist_id = serializers.IntegerField(allow_null=False)
    tracks = serializers.StringRelatedField(many=True)

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


class SongSerializer:
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=64)
    artist_name = serializers.CharField(max_length=128, allow_blank=False)
    album = serializers.StringRelatedField()
