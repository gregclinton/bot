import llm
from importlib import import_module

def run(thread, prompt):
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
        how = [message("system", "\n\n".join(open(f"how/{f}").read() for f in thread["installed"]))]
        completion = llm.invoke(how + messages, thread.get("model"), thread.get("temperature"))

        if count > 10:
            content = "Could you please rephrase that?"
        elif completion.startswith("tool:"):
            assistant(completion)
            tool = completion.split("tool:")[1].split()[0]
            text = completion.partition("\n")[2]
            try:
                output = import_module(f"tools.{tool}").invoke(text, thread)
                if len(output) > 20000:
                    content = output # for big plots mainly
                else:
                    user(f"From {tool} tool:\n{output}\nHope this helps.")
            except Exception as e:
                user(e)
        else:
            content = completion

    assistant(content)
    return content

thread = {"messages": [], "installed": ["brevity", "install"], "bots": set()}
prompt = "I want to test the chatbot tool. Install it. Then try to connect to http://localhost:8123 and say Hello to it."
prompt = "First install chromadb tool. Then answer: What is Medicare part A all about."
# run(thread, prompt)
