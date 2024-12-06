import llm
from importlib import import_module

def run(thread, prompt):
    def message(role, content):
        if role != "system":
            print(f"{role}:")
            print(f"{content}")
        return { "role": role, "content": content }

    messages = thread["messages"]
    messages.append(message("user", prompt))
    content = None
    bulk = None
    count = 0

    while not content:
        count += 1
        how = [message("system", "\n\n".join(open(f"how/{f}").read() for f in thread["installed"]))]
        completion = llm.invoke(how + messages)
        messages.append(message("assistant", completion))

        if completion.startswith("tool:"):
            tool = completion.split("tool:")[1].split()[0]
            text = completion.partition("\n")[2]
        else:
            tool = None
            content = completion

        if count > 10:
            content = "Could you please rephrase that?"
        elif tool:
            try:
                output = import_module(f"tools.{tool}").invoke(text, thread)
                if len(output) > 20000:
                    bulk = output
                    output = "success"
                messages.append(message("user", output))
            except Exception as e:
                content = str(e)

    messages.append(message("assistant", content))
    return { "content": bulk or content }

thread = {"messages": [], "installed": {"brevity", "install"}, "bots": set()}
print(run(thread, "Look up Medicare part A in chromadb database.")["content"])
