import chat

async def run(mode: str, thread: dict):
    """Take a snapshot of the current thread or reset. Mode can be "current" or "reset"."""
    print(f"snap {mode}", flush = True)
    chat.snap(None if mode == "reset" else thread)
    return f"Snapshot {'reset' if mode == 'reset' else 'taken'}."