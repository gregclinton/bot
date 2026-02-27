from pathlib import Path
from types import SimpleNamespace
from datetime import datetime

workspace = Path("/tmp")
messages = workspace / "messages"

# /workspace/messages/box/order-poster

def archive(owner):
    msgs = []
    for box in messages.iterdir():
        if box.is_dir():
            for msg in box.iterdir():
                if owner in [box.name, msg.name.split('-')[1]]:
                    msgs.append(msg)

    msgs.sort(key = lambda m: m.name.split('-')[0])

    for msg in msgs:
        order, poster = msg.name.split('-')
        yield SimpleNamespace(
            to = msg.parent.name,
            poster = poster,
            body = msg.read_text(),
            order = int(order)
            time = datetime.fromtimestamp(msg.stat().st_mtime)
        )

def inbox(owner):
    read = messages / owner / "read"
    start = int(read.read_text()) if read.exists() else 0
    end = start

    for msg in archive(owner):
        if msg.order > start:
            end = max([end, msg.order])
            yield msg

    read.write_text(end)

def post(to, poster, body):
    box = messages / to
    box.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    order = (int(last.read_text()) if last.exists() else 1000000) + 1
    (box / f"{order}-{poster}").write_text(body)
    last.write_text(str(order))

import sys

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"post": post}[name](*args)