from furl import furl
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse

from .fields import UUIDHyperlinkedIdentityField
from .models import Album, Artist, Track, Playlist, PlaylistTrack


class TrackAlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class TrackAlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = TrackAlbumArtistSerializer()

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "artist")


class TrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")
    album = TrackAlbumSerializer()

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number", "album")


class AlbumTrackSerializer(TrackSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="track-detail")

    class Meta:
        model = Track
        fields = ("uuid", "url", "name", "number")


class AlbumArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name")


class AlbumSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="album-detail")
    artist = AlbumArtistSerializer()
    tracks = AlbumTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("uuid", "url", "name", "year", "artist", "tracks")


class ArtistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    url = UUIDHyperlinkedIdentityField(view_name="artist-detail")
    albums_url = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("uuid", "url", "name", "albums_url")

    def get_albums_url(self, artist):
        path = drf_reverse("album-list", request=self.context["request"])
        return furl(path).set({"artist_uuid": artist.uuid}).url


class PlaylistTrackSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    track_id = serializers.IntegerField(source='track.id')
    track_name = serializers.CharField(source='track.name')

    class Meta:
        model = PlaylistTrack
        fields = ['uuid', 'track_id', 'track_name', 'sequence_number']


class PlaylistSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    tracks = PlaylistTrackSerializer(many=True, read_only=True, source='playlisttrack_set')

    class Meta:
        model = Playlist
        fields = ['uuid', 'name', 'tracks']
    