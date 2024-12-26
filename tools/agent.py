import chat

name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[name] = data = tools.get(name, {})
    data["agents"] = agents = data.get("agents", {})
    agents.clear()

def run(name: str, tools: str, docs, prompt: str, thread: dict):
    """
    Creates an agent, or uses an existing agent with a comma-delimeted set of tools
    and a comma-delimeted set of docs. The agent will respond to the prompt.
    When finished with the agent, sign off by saying 'bye'.
    """
    agents = thread["tools"][name]["agents"]

    if name not in agents:
        agents[name] = chat.reset({ "use": { "docs": docs, "tools": tools } })

    return chat.run(prompt, agents[name]) 
