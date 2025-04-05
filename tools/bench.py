import tool

async def run(tools: str, thread: dict):
    "Provide comma separated list of tools such as: bench,consult,shell,model or 'none'."
    print(f"bench: {tools}")
    thread["tools"] = [] if tools == "none" else tool.create(tools.split(','))
    return f"Added tools: {tools}."