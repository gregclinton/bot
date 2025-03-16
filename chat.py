import llm

def reset(thread):
    thread["messages"] = [{ "role": "system", "content": "" }]
    thread["runs"] = []
    return llm.reset(thread)

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role} ({thread['worker' if role == 'assistant' else 'user']}):\n{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]
    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply

if __name__ == "__main__":
    # . ./secrets
    # run("Write a python program foo.py to output the name of a random fruit. Then run it and tell me what fruit it picked.", reset({}))
    run("Hello. When is the Amtrak 228 due to arrive today?", reset({"user": "me", "worker": "hal"}))
