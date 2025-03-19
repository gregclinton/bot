import chat
import os

def run(assistant: str, thread: dict):
    "Hands over the chat to another assistant."
    if os.path.exists(f"assistants/{assistant}"):
        chat.handover(assistant, thread)
        return f"Hello, this is {assistant}. How can I help you?"
    else:
        return f"Sorry, I don't know {assistant}."
