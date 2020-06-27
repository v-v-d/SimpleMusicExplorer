from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Artist
from .serializers import ArtistSerializer, ArtistCreateSerializer


class CustomerAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = request.parser_context['kwargs']['pk']
        user = Artist.objects.filter(id=pk).first().user_id
        if user == request.user.id and request.user.is_artist:
            return True
        return False


class ArtistListView(APIView):
    """Вывод списка всех артистов"""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class ArtistView(APIView):
    """Вывод и создание артиста"""

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        artist = Artist.objects.filter(user=request.user)
        serializer = ArtistSerializer(artist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialize = ArtistCreateSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save(user=request.user)
            return Response(status=201)
        return Response(status=400)


class ArtistDetail(APIView):
    """Показ, редактирование и удаление одного артиста"""

    permission_classes = [permissions.IsAuthenticated, CustomerAccessPermission]

    def get(self, request, pk):
        artist = Artist.objects.get(user_id=request.user.id, id=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request, pk):
        artist_update = Artist.objects.filter(id=pk)
        serialize = ArtistCreateSerializer(data=request.data)
        if serialize.is_valid():
            artist_update.update(**serialize.validated_data)
            return Response(status=201)
        return Response(status=400)

    def delete(self, request, pk):
        artist_delete = Artist.objects.filter(id=pk)
        artist_delete.delete()
        return Response(status=204)