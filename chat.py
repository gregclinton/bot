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
    if any(model.startswith(x) for x in ["gpt", "o1", "o3"]):
        provider = "openai"
    elif model.startswith("claude-"):
        provider = "anthropic"
    elif any(model.startswith(x) for x in ["gemini-", "gemma-"]):
        provider = "google"
    elif "nemotron" in model:
        provider = "nvidia"
    elif "mistral" in model:
        provider = "mistral"
    elif "grok" in model:
        provider = "xai"
    elif "deepseek" in model:
        provider = "together"
    elif model == "phi-4":
        provider = "deepinfra"
        model = "microsoft/" + model
    else:
        provider = "groq"

    if model == "gpt-4.5":
        model += "-preview"
    elif model.startswith("deepseek"):
        model = "deepseek-ai/" + model
    elif model.startswith(("mistral-", "claude-")):
        model += "-latest"
    elif model == "grok-2":
        model += "-1212"
    elif model == "llama-3.3-nemotron-super":
        model = "nvidia/llama-3.3-nemotron-super-49b-v1"
    elif model.startswith("qwq-"):
        model = "qwen-" + model

    thread["provider"] = provider
    thread["model"] = model

    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)

if __name__ == "__main__":
    # . ./secrets
    prompt = "Hello. When is the Amtrak 228 due to arrive today?"
    run(prompt, reset({"user": "me", "assistant": "hal"}))
