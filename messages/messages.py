from types import SimpleNamespace
import storage

messages = storage.root / "messages"
messages.mkdir(parents = True, exist_ok = True)

# messages/to/order-frm   body

def inbox(to):
    folder = messages / to
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
                yield SimpleNamespace(
                    frm = frm,
                    to = path.parent.name,
                    body = path.read_text(),
                    order = int(order),
                    timestamp = int(path.stat().st_mtime)
                )

def post(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n---------------------------\n", flush = True)
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    order = (int(last.read_text()) if last.exists() else 1000000) + 1
    (folder / f"{order}-{frm}").write_text(body)
    last.write_text(str(order))