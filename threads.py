from datetime import datetime, timedelta
from pathlib import Path

start = datetime.now() - timedelta(days = 1)

def get(inbox):
    global start

    for p in Path(inbox).iterdir():
        if p.is_file() and datetime.fromtimestamp(p.stat().st_mtime) > start:
            start = datetime.now()
            return p

    start = datetime.now()