from pathlib import Path

def get(owner):
    # /tmp/threads/owner/correspondent/order-poster
    # /tmp/threads/owner/correspondent/mark

    for thread in Path(f"/tmp/threads/{owner}").iterdir():
        mark = thread / "mark"
        last = False

        for msg in thread.iterdir():
            if msg.name != "mark" and not msg.name.endswith(owner):
                last = msg.name.split("-")[0]

        if last and (not mark.exists() or last > mark.read_text()):
            mark.write_text(last)
            return "Hello."

    return False
