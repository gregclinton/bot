# https://platform.openai.com/docs/api-reference/chat

import requests
import os
import json
import tool

def reset(thread):
    return tool.reset(thread)

def post(payload):
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['GROQ_API_KEY'],
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
    bench = tool.create(thread)
    messages = thread["messages"]
    model = "llama-3.3-70b-versatile"
    model = "qwen-2.5-32b"
    model = "gemma2-9b-it"

    if os.path.exists("notes"):
        messages[0]["content"] = open("notes").read()
    else:
        messages[0]["content"] = ""

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