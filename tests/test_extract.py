from unittest.mock import patch, MagicMock
from scripts import extract


@patch("scripts.extract.spotipy")
def test_get_songs_success(mock_spotipy):
    dummy_song_list = {
        "items": [
            {
                "track": {
                    "album": {
                        "id": "6egzU9NKfora01qaNbvwfZ",
                        "name": "LAST CHRISTMAS",
                        "release_date": "1984-11-29",
                        "total_tracks": 3,
                    },
                    "artists": [{"id": "5lpH0xAS4fVfLkACg9DAuM", "name": "Wham!"}],
                    "duration_ms": 262960,
                    "id": "2FRnf9qhLbvw8fu4IBXx78",
                    "name": "Last Christmas",
                    "popularity": 96,
                }
            }
        ]
    }
    mock_response = MagicMock()
    mock_response.playlist_items.return_value = dummy_song_list
    mock_spotipy.Spotify.return_value = mock_response

    assert extract.get_songs() == dummy_song_list


@patch("scripts.extract.spotipy")
def test_get_songs_exception(mock_spotipy):
    mock_response = MagicMock()
    mock_response.playlist_items.side_effect = Exception("Generic exception message")
    mock_spotipy.Spotify.return_value = mock_response

    assert extract.get_songs() == {}
