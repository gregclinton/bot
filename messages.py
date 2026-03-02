from types import SimpleNamespace
from datetime import datetime
import storage
import sys

messages = storage.root / "messages"
messages.mkdir(parents = True, exist_ok = True)

# /workspace/messages/owner/order-poster

def inbox(owner):
    folder = messages / owner
    folder.mkdir(parents = True, exist_ok = True)

    read = folder / "read"
    start = int(read.read_text()) if read.exists() else 0
    end = start

    for path in folder.iterdir():
        if '-' in path.name:
            order, frm = path.name.split('-')
            if int(order) > start:
                msg = SimpleNamespace(
                    frm = frm,
                    to = path.parent.name,
                    body = path.read_text(),
                    order = int(order),
                    time = datetime.fromtimestamp(path.stat().st_mtime),
                    path = path
                )
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