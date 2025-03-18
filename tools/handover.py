import chat
import os

handovers = [f for f in os.listdir("assistants") if "handover" in open(f"assistants/{f}").readline()]

def run(assistant: str, thread: dict):
    f"Hands over the chat to another assistant. These assistants can accept a handover of the chat: {','.join(handovers)}."
    for handover in handovers:
        if assistant.lower() == handover.lower():
            assistant = handover
            break

    chat.handover(assistant, thread)
    return f"Hello, this is {assistant}. How can I help you?"
