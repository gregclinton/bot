import llm
import tool

def reset(thread):
    spec = open(f"assistants/{thread['assistant']}").read().split("\n")
    tokens = spec[0].split(' ')
    tools = tokens[1:]
    thread["model"] = tokens[0]
    thread["tools"] = tool.create(tools)
    tool.reset(tools, thread)
    thread["messages"] = [{ "role": "system", "content": "\n".join(spec[1:]) }]
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
    prompt = "Write a python program foo.py to output the name of a random fruit. Then run it and tell me what fruit it picked."
    prompt = "List the files in my current working directory." 
    prompt = "Hello. When is the Amtrak 228 due to arrive today?"
    prompt = "Hello. When is the Amtrak 228 due to arrive today in San Diego?"
    run(prompt, reset({"user": "me", "assistant": "hal"}))
