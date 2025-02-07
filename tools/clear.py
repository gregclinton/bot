import chat

def run(thread: dict):
    "Clears the current thread. Call this tool when you are dismissed."
    if not thread.get("human"):
        thread["messages"].clear()

        for thread in thread["workers"].values():
            run(thread)

    return "Success."
