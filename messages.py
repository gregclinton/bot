from pathlib import Path

workspace = Path("/tmp")
messages = workspace / "messages"

# /workspace/messages/box/order-poster
# python3 messages.py post Hal Chief "$(cat hal.md)"
# python3 messages.py post Hal CX143623 "My name is Fred."

def mine(me):
    for box in messages.iterdir():
        if box.is_dir():
            for msg in box.iterdir():
                if box.name == me or msg.name.split('-')[1] == me:
                    yield msg

def post(to, poster, text):
    box = messages / to
    box.mkdir(parents = True, exist_ok = True)
    last = messages / "last"
    order = (int(last.read_text()) if last.exists() else 10000) + 1
    (box / f"{order}-{poster}").write_text(text)
    last.write_text(str(order))

import sys

if __name__ == "__main__":
    name = sys.argv[1]
    args = sys.argv[2:]
    {"post": post}[name](*args)