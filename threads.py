from datetime import datetime
from pathlib import Path

start = datetime.now()

def get(inbox):
    global start

    for p in Path("/tmp/threads/" + inbox).iterdir():
        if p.is_file() and datetime.fromtimestamp(p.stat().st_mtime) > start:
            start = datetime.now()
            return open(p).read()

    start = datetime.now()