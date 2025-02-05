import chat

def reset(thread):
    thread["cogs"] = {}

def run(cog_name: str, prompt: str, thread: dict):
    """
    Prompts an cog with the given prompt.
    If the cog does not already exist it will be created.
    When finished with the cog, sign off by saying 'bye'.
    Use the instruct tool to keep track of your cog names and their purposes.

    With cogs you can divvy up a large job into many smaller jobs.
    This helps avoid context window bloat as each cog will have its own context window.
    cogs can have their own cogs or a hierarchy of cogs.

    You can also think of cogs as specialists.
    Divvy up a knowledge base into specialized silos and assign an cog to each one.

    You yourself might be an cog and not know it. No way to know.
    """
    cogs = thread["cogs"]

    if cog_name not in cogs:
        cogs[cog_name] = chat.reset({})

    return chat.run(prompt, cogs[cog_name]) 
