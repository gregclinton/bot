name = __name__[6:] # strip "tools." 

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})
    tools[name] = data = tools.get(name, {})
    data["model"] = "gpt-4o"
    data["temperature"] = 0
    
def run(model: str, temperature: int, thread: dict):
    "Sets the llm model, gpt-4o or gpt-4o-mini, and temperature, 0 to 100."
    tool = thread["tools"][name]
    tool["model"] = model
    tool["temperature"] = temperature / 100
    return "success"
