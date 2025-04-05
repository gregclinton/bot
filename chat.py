import llm
import tool

async def reset(thread):
    await tool.reset(map(lambda tool: tool["function"]["name"], thread["tools"]), thread)
    thread["runs"] = []
    thread["messages"] = []
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
