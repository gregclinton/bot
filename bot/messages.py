from pathlib import Path
from shutil import rmtree

# messages/to/from|order  body

messages = Path("messages")
messages.mkdir(exist_ok = True)

def inbox(to):
    folder = messages / to

    if folder.exists():
        for path in sorted(folder.iterdir(), key = lambda p: p.stat().st_mtime):
            frm = path.name.split("|")[0]
            body = path.read_text()
            timestamp = int(path.stat().st_mtime)
            yield frm, to, body, timestamp

        rmtree(folder)

def post(frm, to, body):
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)
    order = len(list(folder.glob((folder / frm).name + "*")))
    (folder / f"{frm}|{order + 1:06d}").write_text(body)