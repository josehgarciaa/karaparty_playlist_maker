import argparse
import os
from downloader import download_youtube_audio
from audio_processing import normalize_audio
from playlist_config import PlaylistConfig
from ai_recommendation import suggest_songs
from dj_agent import order_playlist
from output import generate_markdown, concatenate_audio


def main():
    parser = argparse.ArgumentParser(description="Party Playlist Builder")
    parser.add_argument('--links', nargs='+', help='YouTube links to download')
    parser.add_argument('--config', type=str, help='Path to playlist.yml')
    parser.add_argument('--ai-suggestions', type=int, default=5, help='Number of AI song suggestions')
    args = parser.parse_args()

    audio_dir = 'audio'
    user_tracks = []
    if args.links:
        for link in args.links:
            print(f"Downloading: {link}")
            download_youtube_audio(link, output_dir=audio_dir)
            # Find the most recent WAV file in the audio directory
            wav_files = [f for f in os.listdir(audio_dir) if f.lower().endswith('.wav')]
            if wav_files:
                latest_file = max([os.path.join(audio_dir, f) for f in wav_files], key=os.path.getctime)
                normalized_path = latest_file.replace('.wav', '_normalized.wav')
                print(f"Normalizing: {latest_file} -> {normalized_path}")
                normalize_audio(latest_file, normalized_path)
                # Use filename (without extension) as query for metadata
                user_tracks.append({'query': os.path.splitext(os.path.basename(latest_file))[0]})
            else:
                print("No WAV file found to normalize.")
    else:
        print("No YouTube links provided.")

    if args.config:
        print(f"Using playlist config: {args.config}")
        config = PlaylistConfig(args.config)
        theme = config.get_theme()
        rules = config.get_rules()
        blocks = config.get_blocks()
        print(f"\nAI Song Suggestions for theme '{theme}':")
        ai_suggestions = suggest_songs(theme, rules, num_songs=args.ai_suggestions)
        ai_tracks = [{'query': s.split(':')[0].split('-')[0].strip()} for s in ai_suggestions]
        for s in ai_suggestions:
            print(s)
        # Combine user and AI tracks
        all_tracks = user_tracks + ai_tracks
        # Order playlist
        ordered = order_playlist(all_tracks, blocks, rules)
        print("\nOrdered Playlist:")
        for i, track in enumerate(ordered, 1):
            print(f"{i}. {track.get('title', track.get('query', ''))} - {track.get('artist', '')} [Block: {track.get('block', '')}]")
        # Output to Markdown
        md_path = 'ordered_playlist.md'
        generate_markdown(ordered, md_path)
        print(f"\nPlaylist written to {md_path}")
        # Concatenate audio files in playlist order
        wav_files = []
        for track in ordered:
            # Look for normalized WAV file in audio dir
            base = track.get('query', '')
            norm_path = os.path.join(audio_dir, base + '_normalized.wav')
            if os.path.exists(norm_path):
                wav_files.append(norm_path)
        if wav_files:
            concat_path = 'party_playlist.wav'
            concatenate_audio(wav_files, concat_path)
        else:
            print("No normalized audio files found for concatenation.")
    else:
        print("No playlist.yml config provided.")

if __name__ == "__main__":
    main() 