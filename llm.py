# https://platform.openai.com/docs/api-reference/chat

import requests
import os
import json
import tool

def reset(thread):
    return tool.reset(thread)

def post(payload):
    if payload["model"].startswith("gpt"):
        url_base = "https://api.openai.com"
        key = os.environ['OPENAI_API_KEY']
    else:
        url_base = f"https://api-inference.huggingface.co"
        key = os.environ['HUGGINGFACE_API_KEY']

    res = requests.post(
        f"{url_base}/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + key,
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
    model = "gpt-4o"
    model = "Qwen/Qwen2.5-72B-Instruct"
    model = "deepseek/deepseek_v3"

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

        if not content:
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