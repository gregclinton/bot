import chat

async def run(mode: str, thread: dict):
    "Take a snapshot of the current thread or reset. Mode can be "current" or "reset".
    print(f"snap {mode}")
    chat.snap(thread, mode)
    return "Snapshot taken."