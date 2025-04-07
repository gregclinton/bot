import tool

async def run(tools: str, thread: dict):
    "Provide comma separated list of tools such as: bench,consult,shell,model or 'none'."
    print(f"{thread['assistant']}: bench: {tools}", flush = True)
    thread["tools"] = [] if tools == "none" else tools.split(',')
    return f"Added tools: {tools}."