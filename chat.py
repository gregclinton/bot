import llm
import copy

snapshot = None

def create():
    return copy.deepcopy(snapshot)

async def run(prompt, thread):
    messages = thread["messages"] = thread.get("messages", [])
    runs = thread["runs"] = thread.get("runs", [])
    runs.append(len(messages))
    message = lambda role, content: { "role": role, "content": content }
    messages.append(message("user", prompt))
    reply = await llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply

def back(thread):
    runs = thread.get("runs", [])
    if runs:
        del thread["messages"][runs.pop():]

def set_model(thread, provider, model):
    thread["provider"] = provider
    thread["model"] = model
    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)

def snap(thread):
    global snapshot

    if thread:
        snapshot = copy.deepcopy(thread)
        back(snapshot) # remove snap invocation from snapshot
        snapshot.pop("runs", None)
    else:
        snapshot = {
            "user": "me",
            "assistant": "hal",
            "provider": "openai",
            "model": "gpt-4.1-nano",
            "tools": ["bench","shell","snap","consult","model"],
        }

snap(None)