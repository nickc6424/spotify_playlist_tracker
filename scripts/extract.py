import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
from requests.exceptions import HTTPError
from helper_functions import read_config


def get_songs() -> dict:
    """Retrieves API response from Spotify for specific playlist"""
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=read_config("secrets.cfg", "spotify", "spotify_client_id"),
            client_secret=read_config("secrets.cfg", "spotify", "spotify_client_secret"),
            redirect_uri="http://example.com",
            scope="playlist-read-private",
        )
    )
    playlist_id = "spotify:playlist:" + read_config("secrets.cfg", "spotify", "playlist_id")
    fields = "items.track.id, items.track.name, items.track.popularity, items.track.duration_ms, items.track.artists.id, items.track.artists.name, items.track.album.id, items.track.album.name, items.track.album.release_date, items.track.album.total_tracks"
    try:
        return sp.playlist_items(playlist_id=playlist_id, fields=fields)
    except:
        return {}


if __name__ == "__main__":
    songs = get_songs()
    print(songs)
