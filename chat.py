import llm

snapshot = None

async def run(prompt, thread):
    message = lambda role, content: { "role": role, "content": content }
    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = await llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply
