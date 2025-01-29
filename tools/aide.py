import chat

def reset(thread):
    thread["aides"] = {}

def run(name: str, prompt: str, thread: dict):
    """
    Prompts a aide with the given prompt.
    If the aide does not already exist it will be created.
    When finished with the aide, sign off by saying 'bye'.
    Use the instruct tool to keep track of aide names and their purpose.
    """
    aides = thread["aides"]

    if name not in aides:
        aides[name] = chat.reset({})

    return chat.run(prompt, aides[name]) 
