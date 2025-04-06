import chat

async def run(thread: dict):
    "Take a snapshot of the current thread."
    print("snap")
    chat.snapshot = thread.copy()
    chat.snapshot["messages"] = thread["messages"].copy()
    chat.back(chat.snapshot) # remove snap invocation from snapshot
    chat.snapshot["runs"] = []
    return "Snapshot taken."