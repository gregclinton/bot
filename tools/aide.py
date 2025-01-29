import chat

def reset(thread):
    thread["aides"] = {}

def run(aide_name: str, prompt: str, thread: dict):
    """
    Prompts an aide with the given prompt.
    If the aide does not already exist it will be created.
    When finished with the aide, sign off by saying 'bye'.
    Use the instruct tool to keep track of aide names and their purposes.
    """
    aides = thread["aides"]

    if aide_name not in aides:
        aides[aide_name] = chat.reset({})

    return chat.run(prompt, aides[aide_name]) 
