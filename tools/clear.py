import chat

def run(thread: dict):
    "Clears the current thread. Call this tool whenever the incoming prompt indicates farewell, thanks, understood, etc."
    if not thread.get("human"):
        thread["messages"] = thread["messages"][:1]

        for thread in thread["workers"].values():
            run(thread)

        return "Goodbye!"
    else:
        return "You're welcome!"
