from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys

workspace = Path("/tmp")
messages = workspace / "messages"

# /workspace/messages/owner/order-poster

def create_message(msg):
    order, frm = msg.name.split('-')

    return SimpleNamespace(
        frm = frm,
        to = msg.parent.name,
        body = msg.read_text(),
        order = int(order),
        time = datetime.fromtimestamp(msg.stat().st_mtime)
    )

def archive(owner):
    msgs = []
    for box in messages.iterdir():
        if box.is_dir():
            for msg in box.iterdir():
                if '-' in msg.name and owner in [box.name, msg.name.split('-')[1]]:
                    msgs.append(create_message(msg))

    msgs.sort(key = lambda msg: msg.order)

    for msg in msgs:
        yield msg

def inbox(owner):
    folder = messages / owner
    folder.mkdir(parents = True, exist_ok = True)

    read = folder / "read"
    start = int(read.read_text()) if read.exists() else 0
    end = start

    for f in folder.iterdir():
        if '-' in f.name:
            msg = create_message(f)
            if msg.order > start:
                end = max([end, msg.order])
                read.write_text(str(end))
                yield msg

def post(frm, to, body):
    box = messages / to
    box.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    order = (int(last.read_text()) if last.exists() else 1000000) + 1
    (box / f"{order}-{frm}").write_text(body)
    last.write_text(str(order))

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"post": post}[name](*args)