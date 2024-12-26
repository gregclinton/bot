import chat

def run(thread: dict):
    "Clears the current thread. Call this tool whenever the incoming prompt indicates farewell, thanks, understood, etc."
    if not thread.get("human"):
        chat.reset(thread)
        return "Goodbye!"
    else:
        return "You're welcome!"
