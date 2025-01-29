import chat

def reset(thread):
    thread["aides"] = {}

def run(aide_name: str, prompt: str, thread: dict):
    """
    Prompts an aide with the given prompt.
    If the aide does not already exist it will be created.
    When finished with the aide, sign off by saying 'bye'.
    Use the instruct tool to keep track of your aide names and their purposes.

    With aides you can divvy up a large job into many smaller jobs.
    This helps avoid context window bloat as each aide will have its own context window.
    Aides can have their own aides or a hierarchy of aides.

    You can also think of aides as specialists.
    Divvy up a knowledge base into specialized silos and assign an aide to each one.

    You yourself might be an aide and not know it. No way to know.
    """
    aides = thread["aides"]

    if aide_name not in aides:
        aides[aide_name] = chat.reset({})

    return chat.run(prompt, aides[aide_name]) 
