from pathlib import Path

def get(inbox):
    # /tmp/threads/owner/correspondent/order-poster
    # /tmp/threads/owner/correspondent/bookmark

    folder = f"/tmp/threads/{inbox}"

    for thread in Path(folder).iterdir():
        bookmark = f"{str(thread.resolve())}/bookmark"

        for msg in thread.iterdir():
            if msg.name == "bookmark":
                continue
            elif not msg.name.endswith(inbox):
                last = msg.name.split("-")[0]

        if last > open(bookmark).read():
            open(bookmark, "w").write(last)
            return "Hello."
