import requests
import os
import json
import tool

def invoke(thread):
    content = None
    count = 0
    messages = thread["messages"]
    model = thread["model"]
    gpt = model.startswith("gpt")
    url = f"https://api.{'openai.com' if gpt else 'groq.com/openai'}/v1/chat/completions"
    key = os.environ['OPENAI_API_KEY' if gpt else 'GROQ_API_KEY']

    while not content and count < 10:
        count += 1
        res = requests.post(
            url,
            headers = {
                'Authorization': 'Bearer ' + key,
                'Content-Type': 'application/json'
            },
            json = {
            "model": model,
            "temperature": 0,
            "messages": messages,
            "tools": thread["tools"],
            "tool_choice": "auto"
        })

        try:
            res.raise_for_status()
            message = res.json()["choices"][0]["message"]
            messages.append(message)
            content = message.get("content")

            for call in message.get("tool_calls", []):
                fn = call["function"]
                name = fn["name"]
                args = json.loads(fn["arguments"])
                args["thread"] = thread
                output = tool.run(name, args)

                if name == "handover":
                    messages.pop() # remove the tool call message
                    content = output
                    break
                elif name != "consult":
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
        except Exception as e:
            content = str(e)

    return content or "Could you rephrase that, please?"