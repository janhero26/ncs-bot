import json
from pathlib import Path

import yt_dlp

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLRBp0Fe2Gpgn8Y9qI-p0aTxVtw8onBSFj"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "songs.json"


def fetch_playlist():
    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(PLAYLIST_URL, download=False)

    songs = [
        {"title": entry["title"], "video_id": entry["id"]}
        for entry in info["entries"]
        if entry and entry.get("title")
    ]

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(songs)} songs to {OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_playlist()