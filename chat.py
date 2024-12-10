import llm
import tools.chromadb

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role}:\n{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]
    messages.append(message("user", prompt))
    docs = [message("system", "\n\n".join(open(f"docs/{f}").read() for f in thread["docs"]))]
    reply = llm.invoke(docs + messages, thread)
    messages.append(message("assistant", reply))
    return reply
