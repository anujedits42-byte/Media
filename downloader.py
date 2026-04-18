import yt_dlp
import uuid
from pathlib import Path

BASE = Path("downloads")
BASE.mkdir(exist_ok=True)

def download(url, quality, hook):
    folder = BASE / uuid.uuid4().hex
    folder.mkdir()

    fmt_map = {
        "360": "18",
        "720": "22",
        "1080": "137+140",
        "best": "bv*+ba/best"
    }

    ydl_opts = {
        "format": fmt_map.get(quality, "best"),
        "outtmpl": str(folder / "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "progress_hooks": [hook],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return list(folder.glob("*")), folder
