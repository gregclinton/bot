import chat

modeule_name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[modeule_name] = data = tools.get(modeule_name, {})
    data["specialists"] = specialists = data.get("specialists", {})
    specialists.clear()

def run(specialist_name: str, instructions: str, prompt: str, thread: dict):
    """
    Creates a specialist with the given system message instructions or uses an existing specialist.
    The specialist will respond to the prompt.
    When finished with the specialist, sign off by saying 'bye'.
    """
    specialists = thread["tools"][modeule_name]["specialists"]

    if specialist_name not in specialists:
        thread = chat.reset({})
        thread["messages"][0]["content"] = instructions
        specialists[specialist_name] = thread

    return chat.run(prompt, specialists[specialist_name]) 
