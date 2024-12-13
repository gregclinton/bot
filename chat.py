import llm

def reset(thread):
    thread["messages"] = []
    thread["runs"] = []
    return llm.reset(thread)

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role}:\n{content}\n", flush=True)
        return { "role": role, "content": content }

    thread["runs"].append(len(thread["messages"]))
    messages = thread["messages"]
    messages.append(message("user", prompt))
    instructions = message("system", open("instructions").read())
    reply = llm.invoke([instructions] + messages, thread)
    messages.append(message("assistant", reply))
    return reply
