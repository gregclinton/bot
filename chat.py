import llm
from datetime import datetime

def reset(thread):
    thread["messages"] = [{ "role": "system", "content": "" }]
    thread["runs"] = []
    return llm.reset(thread)

def back(thread):
    del thread["messages"][thread["runs"].pop():]

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role}:\n{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]

    use = (thread["use"]["docs"] if thread.get("use") else open("docs/use").read()).split(",")
    docs = "\n\n".join(open(f"docs/{doc}").read() for doc in use)
    messages[0]["content"] = docs.replace("{today}", datetime.now().strftime("%B %d, %Y"))

    thread["runs"].append(len(thread["messages"]))
    messages.append(message("user", prompt))
    reply = llm.invoke(thread)
    messages.append(message("assistant", reply))
    return reply
