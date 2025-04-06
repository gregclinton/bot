import llm

snapshot = {
    "user": "me",
    "assistant": "hal",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "tools": ["bench","snap"],
    "runs": [],
    "messages": [],
}

def create():
    thread = snapshot.copy();
    thread["messages"] = thread["messages"].copy()
    return thread

async def run(prompt, thread):
    message = lambda role, content: { "role": role, "content": content }
    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = await llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def set_model(thread, provider, model):
    thread["provider"] = provider
    thread["model"] = model
    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)
