import llm

snapshot = {
    "user": "me",
    "assistant": "hal",
    "provider": "openai",
    "model": "gpt-4o-mini",
    "tools": ["bench"],
    "runs": [],
    "messages": [],
}

def create():
    thread = snapshot.copy();
    thread.messages = thread.messages.copy()
    return thread

async def run(prompt, thread):
    message = lambda role, content: { "role": role, "content": content }
    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = await llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply
