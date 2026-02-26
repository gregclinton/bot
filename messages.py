from pathlib import Path
from types import SimpleNamespace

workspace = Path("/tmp")
messages = workspace / "messages"

# /workspace/messages/box/order-poster

def mine(me):
    msgs = [
        msg
        for box in messages.iterdir() if box.is_dir()
        for msg in box.iterdir()
        if box.name == me or msg.name.split('-')[1] == me
    ]    

    for msg in sorted(msgs, key = lambda m: m.name.split('-')[0]):
        yield SimpleNamespace(
            to = msg.parent.name,
            poster = msg.name.split('-')[1],
            text = msg.read_text(),
            time = msg.stat().st_mtime
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