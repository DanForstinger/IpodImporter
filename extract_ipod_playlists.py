#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
from pyItunes import iTunesDB
from mutagen import File

def safe_filename(name: str) -> str:
    """Remove unsafe filename characters."""
    return "".join(c for c in name if c.isalnum() or c in " ._-").strip()

def copy_playlist(playlist, music_root, output_root):
    playlist_folder = output_root / safe_filename(playlist.name)
    playlist_folder.mkdir(parents=True, exist_ok=True)

    for index, track in enumerate(playlist.tracks, start=1):
        src = Path(music_root) / track.location.strip("/")
        if not src.exists():
            continue

        try:
            audio = File(src, easy=True)
            title = audio.get("title", [track.Title or src.stem])[0]
            artist = audio.get("artist", [track.Artist or "Unknown Artist"])[0]
        except Exception:
            title = track.Title or src.stem
            artist = track.Artist or "Unknown Artist"

        new_name = f"{str(index).zfill(2)}_{safe_filename(title)}_{safe_filename(artist)}{src.suffix.lower()}"
        dest = playlist_folder / new_name

        shutil.copy2(src, dest)
        print(f"✅ {playlist.name}: {new_name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_ipod_playlists.py /path/to/iPodRoot")
        sys.exit(1)

    ipod_root = Path(sys.argv[1]).expanduser().resolve()
    db_path = ipod_root / "iPod_Control" / "iTunes" / "iTunesDB"
    music_root = ipod_root / "iPod_Control" / "Music"
    output_root = Path.cwd() / "iPod_Playlists"

    if not db_path.exists():
        print(f"❌ Could not find iTunesDB at {db_path}")
        sys.exit(1)

    output_root.mkdir(exist_ok=True)

    print(f"📂 Reading playlists from {db_path}...")
    db = iTunesDB(db_path)
    playlists = db.getPlaylists()

    for playlist in playlists:
        if playlist.tracks:
            copy_playlist(playlist, music_root, output_root)

    print(f"\n🎉 Done! All playlists copied to {output_root}")

if __name__ == "__main__":
    main()
