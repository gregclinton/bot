import os

assistants = os.listdir("assistants")

def run(assistant: str, thread: dict):
    f"""
    Hands over the chat to another assistant.
    These assistants can accept a handover of the chat: {','.join(assistants)}.
    Use the assistant name from this list that most closely matches the requested assistant.
    """
    for name in assistants:
        if name.lower() == assistant.lower():
            assistant = name
            break

    spec = open(f"assistants/{assistant}").read().split("\n")
    tokens = spec[0].split(' ')
    thread["provider"] = tokens[0]
    model = tokens[1]
    tools = tokens[2:]
    thread["messages"][0]["content"] = "\n".join(spec[1:])
    thread["model"] = model
    thread["tools"] = tool.create(tools)
    return f"Hello, this is {assistant}. How can I help you?"