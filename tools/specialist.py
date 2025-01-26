import chat

modeule_name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[modeule_name] = data = tools.get(modeule_name, {})
    data["specialists"] = specialists = data.get("specialists", {})
    specialists.clear()

def run(specialist_name: str, tools: str, docs: str, prompt: str, thread: dict):
    """
    Creates an specialist, or uses an existing specialist with a comma-delimeted set of tools
    and a comma-delimeted set of docs. The specialist will respond to the prompt.
    When finished with the specialist, sign off by saying 'bye'.
    """
    specialists = thread["tools"][modeule_name]["specialists"]

    if specialist_name not in specialists:
        specialists[specialist_name] = chat.reset({})
        specialists[specialist_name]["use"] = { "docs": docs, "tools": tools }

    return chat.run(prompt, specialists[specialist_name]) 
