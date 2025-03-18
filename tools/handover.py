import chat

def run(assistant: str, thread: dict):
    "Hands over the chat to another assistant."
    chat.handover(assistant, thread)
    return f"This is {assistant}. How can I help you?"
