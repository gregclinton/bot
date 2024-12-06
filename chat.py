import llm
from importlib import import_module

def run(thread, prompt):
    def message(role, content):
        if role != "system":
            print(f"{role}:")
            print(f"{content}\n", flush=True)
        return { "role": role, "content": content }

    messages = thread["messages"]
    assistant = lambda prompt: messages.append(message("assistant", prompt))
    user = lambda prompt: messages.append(message("user", prompt))
    user(prompt)
    content = None
    bulk = None
    count = 0

    while not content:
        count += 1
        how = [message("system", "\n\n".join(open(f"how/{f}").read() for f in thread["installed"]))]
        completion = llm.invoke(how + messages)

        if completion.startswith("tool:"):
            tool = completion.split("tool:")[1].split()[0]
            text = completion.partition("\n")[2]
        else:
            tool = None
            content = completion

        if count > 10:
            content = "Could you please rephrase that?"
        elif tool:
            assistant(completion)
            try:
                output = import_module(f"tools.{tool}").invoke(text, thread)
                if len(output) > 20000:
                    bulk = output
                    output = "success"
                user(output)
            except Exception as e:
                user(str(e))

    assistant(content)
    return { "content": bulk or content }

thread = {"messages": [], "installed": {"brevity", "install"}, "bots": set()}
run(thread, "First install chromadb tool. Then answer: What is Medicare part A all about.")
