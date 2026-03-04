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

    for path in sorted(folder.iterdir(), key = lambda p: p.stat().st_mtime):
        if path.name != "read":
            timestamp = path.stat().st_mtime
            if timestamp > start:
                read.write_text(str(timestamp))
                yield SimpleNamespace(
                    frm = path.name,
                    to = path.parent.name,
                    body = path.read_text(),
                    timestamp = timestamp
                )

def post(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n---------------------------\n", flush = True)
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)
    (folder / frm).write_text(body)