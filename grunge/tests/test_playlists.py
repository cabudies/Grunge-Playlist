from uuid import UUID
from rest_framework import status

from . import BaseAPITestCase
from ..models import Playlist


class PlaylistAPITestCase(BaseAPITestCase):
    def setUp(self):
        self.playlist_data = {'uuid': UUID("9e52205f-9927-4eff-b132-ce10c6f3e0b1"), 'name': 'Playlist 1'}
        self.playlist = Playlist.objects.create(**self.playlist_data)
        self.playlist_url = f'/api/{self.version}/playlists/{self.playlist.id}'

    def test_create_playlist(self):
        response = self.client.post('/api/v1/playlists', self.playlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 2)

    def test_retrieve_playlist(self):
        response = self.client.get(self.playlist_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_playlist(self):
        updated_data = {'name': 'Updated Playlist'}
        response = self.client.patch(self.playlist_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Playlist.objects.get(id=self.playlist.id).name, 'Updated Playlist')

    def test_delete_playlist(self):
        response = self.client.delete(self.playlist_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)
