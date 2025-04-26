# Placeholder for output generation

from pydub import AudioSegment

def generate_markdown(tracklist, output_path):
    """
    Write the ordered playlist to a Markdown file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('# Party Playlist\n\n')
        f.write('| # | Title | Artist | Block |\n')
        f.write('|---|-------|--------|-------|\n')
        for i, track in enumerate(tracklist, 1):
            title = track.get('title', track.get('query', ''))
            artist = track.get('artist', '')
            block = track.get('block', '')
            f.write(f'| {i} | {title} | {artist} | {block} |\n')

def concatenate_audio(wav_files, output_path):
    """
    Concatenate a list of WAV files into a single output WAV file.
    """
    if not wav_files:
        print("No audio files to concatenate.")
        return
    combined = AudioSegment.empty()
    for wav in wav_files:
        try:
            audio = AudioSegment.from_wav(wav)
            combined += audio
        except Exception as e:
            print(f"Error loading {wav}: {e}")
    combined.export(output_path, format="wav")
    print(f"Concatenated audio written to {output_path}") 