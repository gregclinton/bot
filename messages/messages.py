from types import SimpleNamespace
import storage

messages = storage.root / "messages"
messages.mkdir(parents = True, exist_ok = True)

# messages/to/frm   body

def inbox(to):
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)

    read = folder / "read"
    start = float(read.read_text()) if read.exists() else 0.0
    end = start

    for path in folder.iterdir():
        if '-' in path.name:
            frm = path.name
            timestamp = path.stat().st_mtime
            if timestamp > start:
                end = max([end, start])
                read.write_text(str(end))
                yield SimpleNamespace(
                    frm = frm,
                    to = path.parent.name,
                    body = path.read_text(),
                    timestamp = timestamp
                )

def post(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n---------------------------\n", flush = True)
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    timestamp = (float(last.read_text()) if last.exists() else 1000000) + 1
    file = folder / frm
    file.write_text(body)
    last.write_text(str(file.stat().st_mtime))