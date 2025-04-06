import chat

async def run(thread: dict):
    "Take a snapshot of the current thread."
    print("snap")
    chat.snapshot = thread
    return "Snapshot taken."