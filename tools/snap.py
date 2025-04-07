import chat
import copy

async def run(thread: dict):
    "Take a snapshot of the current thread."
    print("snap")
    chat.snapshot = copy.deepcopy(thread)
    chat.back(chat.snapshot) # remove snap invocation from snapshot
    chat.snapshot["runs"] = []
    return "Snapshot taken."