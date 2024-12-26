import chat

def run(thread: dict):
    "Clears the current thread. Call this tool whenever the incoming prompt indicates farewell, thanks, understood, etc."
    chat.reset(thread)
    return "Over and out."