from pathlib import Path

def get(owner):
    # /tmp/threads/owner/correspondent/order-poster
    # /tmp/threads/owner/correspondent/bookmark

    for thread in Path(f"/tmp/threads/{owner}").iterdir():
        bookmark = f"{str(thread.resolve())}/bookmark"

        for msg in thread.iterdir():
            if msg.name != "bookmark" and not msg.name.endswith(owner):
                last = msg.name.split("-")[0]

        if last > open(bookmark).read():
            open(bookmark, "w").write(last)
            return "Hello."
