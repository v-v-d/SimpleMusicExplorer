from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from musicapp.models import ArtistAlbum, AlbumTrack, Artist
from musicapp.permissions import IsOwnerOrReadOnly, IsArtistOrReadOnly
from musicapp.serializers import (
    AlbumSerializer, TrackSerializer, FileSerializer, ArtistSerializer,
    ArtistCreateSerializer
)


class ArtistListView(APIView):
    """
    list all artists
    """
    permission_classes = []
    # permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, context={'request': request}, many=True)
        return Response(serializer.data)


class UserArtistView(APIView):
    """
    create and retrieve user artists
    """
    permission_classes = [permissions.IsAuthenticated, IsArtistOrReadOnly]

    def get(self, request):
        artist = Artist.objects.filter(user=request.user)
        serializer = ArtistSerializer(artist, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialize = ArtistCreateSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ArtistDetail(APIView):
    """
    retrieve, update and delete artists
    """
    permission_classes = [IsArtistOrReadOnly]
    # permission_classes = [permissions.IsAuthenticated, IsArtistOrReadOnly]

    def get(self, request, pk):
        artist = get_object_or_404(Artist, id=pk)
        serializer = ArtistSerializer(artist, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        artist_update = Artist.objects.filter(id=pk)
        serialize = ArtistCreateSerializer(data=request.data)
        if serialize.is_valid():
            artist_update.update(**serialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        artist_delete = Artist.objects.filter(id=pk)
        artist_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumsListView(ListAPIView):
    """
    list all albums
    """
    queryset = ArtistAlbum.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = AlbumSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class AlbumListView(APIView):
    """
    list specific artist albums, or create a new one
    """
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, pk):
        albums = ArtistAlbum.objects.filter(artist=pk).all()
        serializer = AlbumSerializer(albums, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailView(APIView):
    """
    retrieve, update or delete an album
    """
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        album = get_object_or_404(ArtistAlbum, id=pk)
        serializer = AlbumSerializer(album, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        album = get_object_or_404(ArtistAlbum, id=pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        album = get_object_or_404(ArtistAlbum, id=pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        album = get_object_or_404(ArtistAlbum, id=pk)
        serialize = AlbumSerializer(album, data=request.data, partial=True)
        if serialize.is_valid():
            album.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TrackListView(APIView):
    """
    lists and add tracks on specific album
    """
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        tracks = AlbumTrack.objects.filter(album_id=pk).all()
        serializer = TrackSerializer(tracks, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = TrackSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        track = get_object_or_404(AlbumTrack, id=pk)
        serialize = TrackSerializer(track, data=request.data, partial=True)
        if serialize.is_valid():
            track.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        track = AlbumTrack.objects.filter(pk=pk).all()
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
