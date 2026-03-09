from pathlib import Path
from shutil import rmtree

# messages/to/from|order  body

messages = Path("messages")
messages.mkdir(exist_ok = True)

def log(frm, to, body):
    print(f"From: {frm}\nTo: {to}\n{body}\n==========================", flush = True)

def inbox(name):
    folder = messages / name

    if folder.exists():
        for path in sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime):
            yield path.name.split("|")[0], name, path.read_text(), int(path.stat().st_mtime)
        rmtree(folder)

def post(frm, to, body):
    log(frm, to, body)
    folder = messages / to
    folder.mkdir(exist_ok = True)
    order = len(list(folder.glob((folder / frm).name + "*")))
    (folder / f"{frm}|{order + 1:06d}").write_text(body)