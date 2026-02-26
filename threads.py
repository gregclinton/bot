from pathlib import Path

def messages(thread):
    for msg in thread.iterdir():
        if msg.name != "mark":
            yield msg

def get(owner):
    # /workspace/threads/owner/correspondent/order-poster
    # /workspace/threads/owner/correspondent/mark
    inbox = Path(f"/tmp/threads/{owner}")
    inbox.mkdir(parents = True, exist_ok = True)

    for thread in inbox.iterdir():
        mark = thread / "mark"
        last = False
        text = ""

        for msg in messages(thread):
            text += msg.read_text()
            text += "\n-----------------------------------------\n"
            if not msg.name.endswith(owner):
                last = msg.name.split("-")[0]

        if last and (not mark.exists() or last > mark.read_text()):
            mark.write_text(last)
            return text

    return False

def post(to, _from, text):
    # /workspace/threads/to/from/order-poster

    thread = Path(f"/tmp/threads/{to}/{_from}")
    thread.mkdir(parents = True, exist_ok = True)
    order = "10000"
    for msg in messages(thread):
        order = msg.name.split("-")[0]
    (thread / f"{order}-{_from}").write_text(text)

import sys

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"post": post}[name](*args)