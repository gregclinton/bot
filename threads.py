from pathlib import Path

def get(owner):
    # /workspace/threads/owner/correspondent/order-poster
    # /workspace/threads/owner/correspondent/mark

    for thread in Path(f"/tmp/threads/{owner}").iterdir():
        mark = thread / "mark"
        last = False
        text = ""

        for msg in thread.iterdir():
            if msg.name != "mark":
                text += msg.read_text()
                text += "\n-----------------------------------------\n"
                if not msg.name.endswith(owner):
                    last = msg.name.split("-")[0]

        if last and (not mark.exists() or last > mark.read_text()):
            mark.write_text(last)
            return text

    return False

def post(to, from, text):
    # /workspace/threads/to/from/order-poster

    thread = Path(f"/tmp/threads/{to}/{from}")
    thread.mkdir(parents = True, exist_ok = True)
    order = "10000"
    for msg in thread.iterdir():
        if msg.name != "mark":
            order = msg.name.split("-")[0]
    (thread / f"{order}-{from}").write_text(text)