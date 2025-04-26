# Party Playlist Builder

## Overview
The Party Playlist Builder is a Python-based tool that automates the creation, organization, and optimization of party playlists. Users submit YouTube links, and the system downloads, processes, and arranges tracks using AI for recommendations and playlist ordering. The final output includes a Markdown tracklist and a high-quality audio file.

## Features
- Download and extract audio from YouTube links at the highest possible quality (WAV).
- Normalize and equalize audio for consistent playback.
- AI-powered song recommendations based on party themes and rules.
- Intelligent DJ agent for playlist ordering (block themes, energy, no repeated artists, etc.).
- Outputs a Markdown file with tracklist and a single concatenated audio file.
- CLI-only interface with progress logs.

## Technologies
- Python 3.8+
- yt-dlp (YouTube downloads)
- pydub & FFmpeg (audio processing)
- OpenAI API (AI recommendations)
- PyYAML (YAML config)

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure FFmpeg is installed and available in your PATH.
4. Prepare your `playlist.yml` configuration file.

## Usage
Run the CLI to start building your playlist:
```bash
python cli.py --links <YouTube_URL_1> <YouTube_URL_2> ... --config playlist.yml
```

## Roadmap
- Phase 1: Core audio pipeline (download, process, store)
- Phase 2: AI recommendations
- Phase 3: DJ agent & ordering
- Phase 4: Extended features & optimization

## License
For testing and personal use only. Copyright handling is the user's responsibility.