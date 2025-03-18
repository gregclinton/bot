import chat

def run(assistant: str, thread: dict):
    "Hands over the chat to another assistant."
    chat.handover(assistant, thread)
    return f"Hello, this is {assistant}. How can I help you?"
