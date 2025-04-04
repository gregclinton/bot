import llm
import tool

async def reset(thread):
    spec = open(f"assistants/{thread['assistant']}").read().split("\n")
    tokens = spec[0].split(' ')
    thread["provider"] = tokens[0]
    model = tokens[1]
    tools = tokens[2:]
    content = "\n".join(spec[1:])
    thread["model"] = model
    thread["tools"] = tool.create(tools)
    await tool.reset(tools, thread)
    thread["messages"] = [
        { "role": "user", "content": content},
        { "role": "assistant", "content": "Yes, proceed."}
    ]
    thread["runs"] = []
    return thread

def back(thread):
    del thread["messages"][thread["runs"].pop():]

async def run(prompt, thread):
    message = lambda role, content: { "role": role, "content": content }
    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = await llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply

def set_model(thread, provider, model):
    thread["provider"] = provider
    thread["model"] = model
    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)
