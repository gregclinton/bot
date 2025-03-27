import llm
import tool

def reset(thread):
    spec = open(f"assistants/{thread['assistant']}").read().split("\n")
    tokens = spec[0].split(' ')
    thread["provider"] = tokens[0]
    model = tokens[1]
    tools = tokens[2:]
    content = "\n".join(spec[1:])
    thread["model"] = model
    thread["tools"] = tool.create(tools)
    tool.reset(tools, thread)
    thread["messages"] = [
        { "role": "user", "content": content},
        { "role": "assistant", "content": "Yes, proceed."}
    ]
    thread["runs"] = []
    return thread

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def run(prompt, thread):
    def message(role, content):
        if role == "user":
            print(f"{thread['user']} to {thread['assistant']}:")
        elif role == "assistant":
            print(f"{thread['assistant']} to {thread['user']}:")
        print(f"{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply

def set_model(thread, model):
    provider = "openai"

    if model == "gpt-4.5":
        model += "-preview"
    elif model.startswith("deepseek-"):
        model = "deepseek-ai/" + model
        provider = "together"
    elif model.startswith("gemini-2.0"):
        model += "-flash"
        provider = "google"
    elif model.startswith("gemini-2.5"):
        model += "-pro-exp-03-25"
        provider = "google"
    elif model.startswith("mistral-"):
        model += "-latest"
        provider = "mistral"
    elif model.startswith("claude-"):
        model += "-sonnet-latest"
        provider = "anthropic"
    elif model.startswith("llama-3.3"):
        model = "nvidia/llama-3.3-nemotron-super-49b-v1"
        provider = "nvidia"

    thread["provider"] = provider
    thread["model"] = model

    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)