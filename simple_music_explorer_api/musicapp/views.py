from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from musicapp.models import AlbumModel, TrackModel, ArtistModel
from musicapp.permissions import IsOwnerOrReadOnly
from musicapp.serializers import AlbumSerializer, TrackSerializer, FileSerializer, ArtistSerializer, \
    ArtistCreateSerializer


class ArtistListView(APIView):
    """Вывод списка всех артистов"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        artists = ArtistModel.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class ArtistView(APIView):
    """Вывод и создание артиста"""

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        artist = ArtistModel.objects.filter(user=request.user)
        serializer = ArtistSerializer(artist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialize = ArtistCreateSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ArtistDetail(APIView):
    """Показ, редактирование и удаление одного артиста"""

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        artist = get_object_or_404(ArtistModel, id=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request, pk):
        artist_update = ArtistModel.objects.filter(id=pk)
        serialize = ArtistCreateSerializer(data=request.data)
        if serialize.is_valid():
            artist_update.update(**serialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        artist_delete = ArtistModel.objects.filter(id=pk)
        artist_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumsListView(APIView):
    """
    list all albums
    """
    def get(self, request):
        albums = AlbumModel.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)


class AlbumListView(APIView):
    """
    list specific artist albums, or create a new one
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        albums = AlbumModel.objects.filter(artist=pk).all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailView(APIView):
    """
    retrieve, update or delete an album
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        serialize = AlbumSerializer(album, data=request.data, partial=True)
        if serialize.is_valid():
            album.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TrackListView(APIView):
    """
    lists and add tracks on specific album
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        tracks = TrackModel.objects.filter(album_id=pk).all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = TrackSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    parser_class = [FileUploadParser]

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
