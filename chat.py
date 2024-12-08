import llm
from importlib import import_module

def run(prompt, thread):
    def message(role, content):
        if role != "system":
            print(f"{role}:\n{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]
    assistant = lambda prompt: messages.append(message("assistant", prompt))
    user = lambda prompt: messages.append(message("user", prompt))
    user(prompt)
    content = None
    count = 0

    while not content:
        count += 1
        docs = [message("system", "\n\n".join(open(f"docs/{f}").read() for f in thread["docs"]))]
        completion = llm.invoke(docs + messages, thread)

        if count > 10:
            content = "Could you please rephrase that?"
        elif completion.startswith("tool:"):
            assistant(completion)
            tool = completion.split("tool:")[1].split()[0]
            text = completion.partition("\n")[2]
            try:
                user(import_module(f"tools.{tool}").run(text, thread))
            except Exception as e:
                user(e)
        else:
            content = completion

    assistant(content)
    return content

thread = {"messages": [], "docs": ["brevity", "docs"], "bots": set()}
prompt = "I want to test the chatbot tool. Install it. Then try to connect to http://localhost:8123 and say Hello to it."
prompt = "First install chromadb tool. Then answer: What is Medicare part A all about."
# run(thread, prompt)
