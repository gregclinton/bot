def run(instructions: str, thread: dict):
    """
    Overwrites the system message with the given instructions.
    """
    thread["messages"][0]["content"] = instructions
    return "success"