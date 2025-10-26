#!/usr/bin/env python3
import os
import sys
import shutil
from mutagen import File
from pathlib import Path

def safe_filename(name: str) -> str:
    """Sanitize filenames by removing forbidden characters."""
    return "".join(c for c in name if c.isalnum() or c in " ._-").strip()

def copy_music_files(ipod_dir: Path, output_dir: Path):
    music_dir = ipod_dir / "iPod_Control" / "Music"
    if not music_dir.exists():
        print(f"❌ Could not find {music_dir}. Make sure you selected the root of your iPod.")
        sys.exit(1)

    supported_exts = {".mp3", ".m4a", ".aac", ".wav", ".flac"}
    count = 0

    for file_path in music_dir.rglob("*"):
        if file_path.suffix.lower() not in supported_exts:
            continue

        try:
            audio = File(file_path, easy=True)
            if not audio:
                continue

            artist = audio.get("artist", ["Unknown Artist"])[0]
            album = audio.get("album", ["Unknown Album"])[0]
            title = audio.get("title", [file_path.stem])[0]

            track_num = audio.get("tracknumber", [""])[0]
            if isinstance(track_num, list):
                track_num = track_num[0]
            track_num = str(track_num).split("/")[0]
            track_str = track_num.zfill(2) if track_num.isdigit() else "00"

            artist_folder = output_dir / safe_filename(artist)
            album_folder = artist_folder / safe_filename(album)
            album_folder.mkdir(parents=True, exist_ok=True)

            new_filename = f"{track_str}_{safe_filename(title)}{file_path.suffix.lower()}"
            dest = album_folder / new_filename

            if not dest.exists():
                shutil.copy2(file_path, dest)
                count += 1
                print(f"✅ Copied: {artist} - {album} - {title}")
        except Exception as e:
            print(f"⚠️ Skipping {file_path.name}: {e}")

    print(f"\n🎵 Done! {count} songs copied to {output_dir}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_ipod_music.py /path/to/iPodRoot")
        sys.exit(1)

    ipod_root = Path(sys.argv[1]).expanduser().resolve()
    output_dir = Path.cwd() / "iPod_Music_Sorted"
    output_dir.mkdir(exist_ok=True)

    copy_music_files(ipod_root, output_dir)

if __name__ == "__main__":
    main()
