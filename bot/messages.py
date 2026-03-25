from pathlib import Path
from shutil import rmtree
import unique
import sys

# messages/to/from|random  body

messages = Path("messages")

def inbox(to):
    folder = messages / to

    if folder.exists():
        for path in sorted(folder.iterdir(), key = lambda p: p.stat().st_mtime):
            frm = path.name.split("|")[0]
            body = path.read_text()
            yield frm, body, path

        rmtree(folder)

def post(frm, to, body):
    unique.path(messages / to, frm).write_text(body)

if __name__ == "__main__":
    globals()[sys.argv[1]](*sys.argv[2:])