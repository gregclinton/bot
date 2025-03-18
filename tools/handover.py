import chat

def run(assistant: str, thread: dict):
    "Hands over the chat to another assistant."
    messages = thread["messages"]
    thread = chat.reset({ "user": "me", "assistant": assistant })
    thread["messages"] = messages + thread["messages"]
    return thread
