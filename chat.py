import llm
import tool

def load(assistant):
    spec = open(f"assistants/{thread['assistant']}").read().split("\n")
    tokens = spec[0].split(' ')
    model = tokens[0]
    tools = tokens[1:]
    content = "\n".join(spec[1:])
    return model, tools, content

def reset(thread):
    model, tools, content = load(thread["assistant"])
    thread["model"] = model
    thread["tools"] = tool.create(tools)
    tool.reset(tools, thread)
    thread["messages"] = [
        { "role": "user", "content": content},
        { "role": "assistant", "content": "Yes, proceed."}
    ]
    thread["runs"] = []
    return thread

def handover(assistant, thread):
    model, tools, content = load(assistant)
    thread["model"] = model
    thread["tools"] = tool.create(tools)
    thread["assistant"] = assistant

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

if __name__ == "__main__":
    # . ./secrets
    prompt = "Hello. When is the Amtrak 228 due to arrive today?"
    run(prompt, reset({"user": "me", "assistant": "hal"}))
