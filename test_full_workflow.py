import unittest
from unittest.mock import patch, MagicMock
import os
from audio_processing import normalize_audio, equalize_audio
from playlist_config import PlaylistConfig
from ai_recommendation import suggest_songs
from dj_agent import order_playlist
from output import generate_markdown, concatenate_audio

class TestPartyPlaylistBuilder(unittest.TestCase):
    def setUp(self):
        # Create dummy audio files for concatenation
        from pydub.generators import Sine
        os.makedirs('audio', exist_ok=True)
        for i in range(3):
            tone = Sine(440 + i*100).to_audio_segment(duration=1000)  # 1 second
            tone.export(f'audio/test{i}_normalized.wav', format='wav')
        self.tracks = [
            {'query': 'test0'},
            {'query': 'test1'},
            {'query': 'test2'}
        ]
        self.blocks = [
            {'name': 'Block1', 'duration': 1, 'instructions': ''},
            {'name': 'Block2', 'duration': 1, 'instructions': ''}
        ]
        self.rules = {}

    def tearDown(self):
        # Clean up generated files
        for i in range(3):
            try:
                os.remove(f'audio/test{i}_normalized.wav')
            except FileNotFoundError:
                pass
        try:
            os.remove('ordered_playlist.md')
        except FileNotFoundError:
            pass
        try:
            os.remove('party_playlist.wav')
        except FileNotFoundError:
            pass
        try:
            os.rmdir('audio')
        except OSError:
            pass

    @patch('ai_recommendation.suggest_songs')
    @patch('metadata.get_metadata')
    def test_full_workflow(self, mock_get_metadata, mock_suggest_songs):
        # Mock AI suggestions
        mock_suggest_songs.return_value = [
            '1. Song A - Artist A: Great for the theme',
            '2. Song B - Artist B: Fits the mood'
        ]
        # Mock metadata
        def fake_metadata(query):
            return {'title': query + '_title', 'artist': query + '_artist'}
        mock_get_metadata.side_effect = fake_metadata

        # Combine user and AI tracks
        ai_tracks = [{'query': 'Song A'}, {'query': 'Song B'}]
        all_tracks = self.tracks + ai_tracks
        ordered = order_playlist(all_tracks, self.blocks, self.rules)
        # Markdown output
        generate_markdown(ordered, 'ordered_playlist.md')
        self.assertTrue(os.path.exists('ordered_playlist.md'))
        # Audio concatenation (only user tracks have files)
        wav_files = [f'audio/test{i}_normalized.wav' for i in range(3)]
        concatenate_audio(wav_files, 'party_playlist.wav')
        self.assertTrue(os.path.exists('party_playlist.wav'))

if __name__ == '__main__':
    unittest.main() 