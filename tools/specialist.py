import chat

def reset(thread):
    thread["specialists"] = {}

def run(name: str, prompt: str, thread: dict):
    """
    Prompts a specialist with the given prompt.
    If the specialist does not already exist it will be created.
    When finished with the specialist, sign off by saying 'bye'.
    Use the instruct tool to keep track of specialist names and their purpose.
    """
    specialists = thread["specialists"]

    if name not in specialists:
        specialists[name] = chat.reset({})

    return chat.run(prompt, specialists[name]) 
