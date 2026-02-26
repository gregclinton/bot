from pathlib import Path
from types import SimpleNamespace

workspace = Path("/tmp")
messages = workspace / "messages"

# /workspace/messages/box/order-poster

def mine(me):
    msgs = []
    for box in messages.iterdir():
        if box.is_dir():
            for msg in box.iterdir():
                if me in [box.name, msg.name.split('-')[1]]:
                    msgs.append(msg)

    msgs.sort(key = lambda m: m.name.split('-')[0])

    for msg in msgs:
        yield SimpleNamespace(
            to=msg.parent.name,
            poster=msg.name.split('-')[1],
            text=msg.read_text(),
            time=msg.stat().st_mtime
        )

def post(to, poster, text):
    box = messages / to
    box.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    order = (int(last.read_text()) if last.exists() else 10000) + 1
    (box / f"{order}-{poster}").write_text(text)
    last.write_text(str(order))

import sys

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"post": post}[name](*args)