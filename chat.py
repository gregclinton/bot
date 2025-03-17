import llm
import tool

def reset(thread):
    spec = open(f"assistants/{thread['assistant']}").read().split("\n")
    tokens = spec[0].split(' ')
    tools = tokens[1:]
    thread["model"] = tokens[0]
    thread["tools"] = tool.create(tools)
    tool.reset(tools, thread)
    thread["messages"] = [
        { "role": "user", "content": "\n".join(spec[1:])},
        { "role": "assistant", "content": "Yes, proceed."}
    ]
    thread["runs"] = []
    return thread

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role} ({thread[role]}):\n{content}\n", flush=True)
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
