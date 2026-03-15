from pathlib import Path
from shutil import rmtree
import sys

# messages/to/from|order  body

messages = Path("messages")

def inbox(to):
    folder = messages / to

    if folder.exists():
        for path in sorted(folder.iterdir(), key = lambda p: p.stat().st_mtime):
            frm = path.name.split("|")[0]
            body = path.read_text()
            timestamp = int(path.stat().st_mtime)
            yield frm, body, timestamp

        rmtree(folder)

def post(frm, to, body):
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)
    order = len(list(folder.glob((folder / frm).name + "*")))
    (folder / f"{frm}|{order + 1:06d}").write_text(body)

def poll(to):
    for frm, body, timestamp in inbox(to):
        print(f"From: {frm}\nTo: {to}\n{body}\n")

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])