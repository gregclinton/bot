import chat

modeule_name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[modeule_name] = data = tools.get(modeule_name, {})
    data["agents"] = agents = data.get("agents", {})
    agents.clear()

def run(agent_name: str, tools: str, docs: str, prompt: str, thread: dict):
    """
    Creates an agent, or uses an existing agent with a comma-delimeted set of tools
    and a comma-delimeted set of docs. The agent will respond to the prompt.
    When finished with the agent, sign off by saying 'bye'.
    """
    agents = thread["tools"][modeule_name]["agents"]

    if agent_name not in agents:
        agents[agent_name] = chat.reset({ "use": { "docs": docs, "tools": tools } })

    return chat.run(prompt, agents[agent_name]) 
