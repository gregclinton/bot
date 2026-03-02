from types import SimpleNamespace
from datetime import datetime
import storage

messages = storage.root / "messages"
messages.mkdir(parents = True, exist_ok = True)

# /workspace/messages/owner/order-poster

def msg_from_path(path):
    order, frm = path.name.split('-')
    return SimpleNamespace(
        frm = frm,
        to = path.parent.name,
        body = path.read_text(),
        order = int(order),
        time = datetime.fromtimestamp(path.stat().st_mtime),
        path = path
    )

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
                end = max([end, int(order)])
                read.write_text(str(end))
                yield msg_from_path(path)

def post(frm, to, body):
    box = messages / to
    box.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    order = (int(last.read_text()) if last.exists() else 1000000) + 1
    (box / f"{order}-{frm}").write_text(body)
    last.write_text(str(order))