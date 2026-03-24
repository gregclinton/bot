from pathlib import Path
from shutil import rmtree
import unique
import chronological

# messages/to/from|random  body

messages = Path("messages")

def inbox(to):
    folder = messages / to

    if folder.exists():
        for timestamp, path in chronological.paths(folder):
            frm = path.name.split("|")[0]
            body = path.read_text()
            yield frm, body, timestamp

        rmtree(folder)

def post(frm, to, body):
    unique.path(messages / to, frm).write_text(body)