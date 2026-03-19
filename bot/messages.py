from pathlib import Path
from shutil import rmtree
import sys
from random import choice

# messages/to/from|random  body

messages = Path("messages")

def inbox(to):
    folder = messages / to

    if folder.exists():
        pairs = [(p.stat().st_mtime, p) for p in folder.iterdir()]
        pairs.sort()

        for timestamp, path in pairs:
            frm = path.name.split("|")[0]
            body = path.read_text()
            yield frm, body, timestamp

        rmtree(folder)

def post(frm, to, body):
    folder = messages / to
    folder.mkdir(parents = True, exist_ok = True)
    while True:
        random = ''.join(choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3))
        path = folder / f"{frm}|{random}"
        if not path.exists():
            path.write_text(body)
            break

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])