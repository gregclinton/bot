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
    thread["provider"] = (
        "openai" if model.startswith(x) for x in ["gpt", "o1", "o3"]
        else "anthropic" if model.startswith("claude-")
        else "google" if model.startswith(x) for x in ["gemini-", "gemma-"]
        else "nvidia" if "nemotron" in model
        else "mistral" if "mistral" in model
        else "together" if "deepseek" in model
        else "microsoft" if model == "phi-4"
        else "groq"
    )
    if model == "gpt-4.5":
        model += "-preview"
    elif model.startswith("deepseek"):
        model = "deepseek-ai" + model
    elif model.startswith("mistral"):
        model += "-latest"
    elif model == "grok-2"
        model += "-1212"

    thread["model"] = model

if __name__ == "__main__":
    # . ./secrets
    prompt = "Hello. When is the Amtrak 228 due to arrive today?"
    run(prompt, reset({"user": "me", "assistant": "hal"}))
