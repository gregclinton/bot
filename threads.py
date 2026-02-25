from datetime import datetime
from pathlib import Path

def get(inbox):
    filetime = lambda p: datetime.fromtimestamp(p.stat().st_mtime)
    folder = f"/tmp/threads/{inbox}"
    bookmark = Path(f"{folder}/bookmark")
    start = filetime(bookmark) if bookmark.exists() else (datetime.now() - timedelta(years=10))

    for p in Path(folder).iterdir():
        if p.is_file() and filetime(p) > start:
            return open(p).read()

    bookmark.touch()