import requests
import os
import json
import tool

# with tools: llama-3.3-70b-versatile qwen-2.5-32b gpt-4o-mini
# no tools: 8K: llama-3.2-3b-preview llama-3.2-1b-preview  128K: llama-3.1-8b-instant

def reset(thread):
    return tool.reset(thread)

def post(payload):
    gpt = payload["model"].startswith("gpt")
    res = requests.post(
        f"https://api.{'openai.com' if gpt else 'groq.com/openai'}/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY' if gpt else 'GROQ_API_KEY'],
            'Content-Type': 'application/json'
        },
        json = payload)

    try:
        res.raise_for_status()
        return res
    except Exception as e:
        return e

def invoke(thread):
    content = None
    count = 0
    bench = []
    messages = thread["messages"]
    worker = open(f"workers/{thread['worker']}").read().split("\n")
    model = worker[0]
    messages[0]["content"] = "\n".join(worker[1:])

    if model in ["qwen-2.5-32b", "llama-3.3-70b-versatile"]:
        bench = tool.create(thread)

    while not content and count < 10:
        count += 1
        res = post({
            "model": model,
            "temperature": 0,
            "messages": messages,
            "tools": bench,
            "tool_choice": "auto"
        })

        if isinstance(res, Exception):
            content = str(res)
        else:
            message = res.json()["choices"][0]["message"]
            content = message.get("content")

            if "tool_calls" in message:
                messages.append(message)

                for call in message.get("tool_calls", []):
                    fn = call["function"]
                    name = fn["name"]
                    args = json.loads(fn["arguments"])
                    args["thread"] = thread

                    try:
                        output = tool.run(name, args)
                    except Exception as e:
                        output = str(e)

                    print(f"{name}:")

                    del args["thread"]

                    [print(arg) for arg in args.values()]
                    print(f"\n{output}\n")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": name,
                        "content": output
                    })

    return content or "Could you rephrase that, please?"