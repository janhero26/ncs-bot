import json
import random
from pathlib import Path

SONGS_PATH = Path(__file__).parent / "data" / "songs.json"

YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}

FFMPEG_OPTIONS = {
    "options": "-vn",
}


def load_songs():
    with open(SONGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_shuffled_queue():
    songs = load_songs()
    random.shuffle(songs)
    return songs