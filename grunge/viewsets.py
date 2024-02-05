from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError

from .filters import AlbumFilter, ArtistFilter, TrackFilter
from .models import Album, Artist, Track, Playlist, PlaylistTrack
from .serializers import AlbumSerializer, ArtistSerializer, TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer


class BaseAPIViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class ArtistViewSet(BaseAPIViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_class = ArtistFilter


class AlbumViewSet(BaseAPIViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_class = AlbumFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("artist").prefetch_related("tracks")


class TrackViewSet(BaseAPIViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_class = TrackFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("album", "album__artist")


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    

    def create_or_update_tracks(self, playlist, tracks_data):
        for track_data in tracks_data:
            track_id = track_data['id']
            try:
                track = Track.objects.get(id=track_id)
                PlaylistTrack.objects.create(playlist=playlist, track=track, sequence_number=track_data['sequence_number'])
            except Track.DoesNotExist:
                raise IntegrityError(
                    f"Track with ID {track_data['id']} does not exist."
                )
            except IntegrityError:
                raise IntegrityError(
                    f"Duplicate combination of playlist_id and sequence_number for track {track_data['id']}."
                )


    def create(self, request, *args, **kwargs):
        tracks_data = request.data.pop('tracks', [])
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            playlist = serializer.save()

            if tracks_data:
                self.create_or_update_tracks(playlist, tracks_data)

            return Response(serializer.data, status=201)
        except IntegrityError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


    def update(self, request, *args, **kwargs):
        tracks_data = request.data.pop('tracks', [])
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            playlist = serializer.save()

            instance.playlisttrack_set.all().delete()

            if tracks_data:
                self.create_or_update_tracks(playlist, tracks_data)

            return Response(serializer.data, status=200)
        except IntegrityError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    

    def destroy(self, request, pk=None, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Playlist.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
