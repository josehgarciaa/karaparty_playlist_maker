# Placeholder for metadata and lyrics retrieval

import requests

MUSICBRAINZ_SEARCH_URL = "https://musicbrainz.org/ws/2/recording/"
GENIUS_SEARCH_URL = "https://api.genius.com/search"
GENIUS_API_TOKEN = None  # Set your Genius API token here or via environment variable


def get_metadata(query):
    """
    Query MusicBrainz for title and artist metadata.
    """
    params = {
        'query': query,
        'fmt': 'json',
        'limit': 1
    }
    try:
        resp = requests.get(MUSICBRAINZ_SEARCH_URL, params=params, headers={'User-Agent': 'PartyPlaylistBuilder/1.0'})
        data = resp.json()
        if data['recordings']:
            rec = data['recordings'][0]
            title = rec.get('title', '')
            artist = rec['artist-credit'][0]['name'] if rec.get('artist-credit') else ''
            return {'title': title, 'artist': artist}
    except Exception as e:
        print(f"MusicBrainz error: {e}")
    return {'title': '', 'artist': ''}


def get_lyrics(title, artist):
    """
    Stub for Genius API lyrics retrieval. Returns empty string for now.
    """
    # To implement: Use GENIUS_API_TOKEN and Genius API for real lyrics
    return ""


def get_bpm(title, artist):
    """
    Stub for BPM retrieval. Returns None for now.
    """
    # To implement: Use Spotify or other API for BPM
    return None 