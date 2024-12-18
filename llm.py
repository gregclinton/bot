# https://platform.openai.com/docs/api-reference/chat

import requests
import os
import json
import tool

def reset(thread):
    return tool.reset(thread)

def post(payload):
    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY'],
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
    bench = tool.open()
    messages = thread["messages"]

    while not content and count < 10:
        count += 1
        model = thread["tools"]["model"]
        res = post({
            "model": model["model"],
            "temperature": model["temperature"],
            "messages": thread["messages"],
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

                if name in ['json']:
                    content = output
                    break
                else:
                    del args["thread"]

                    [print(arg) for arg in args.values()]
                    print(f"\n{output}\n")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "name": name,
                        "content": output
                    })

    tool.close()
    return content or "Could you rephrase that, please?"


def mini(query):
    res = post({
        "model": "gpt-4o-mini",
        "temperature": 0,
        "messages": [{"role": "user", "content": query[:8000]}]
    })

    return str(res) if isinstance(res, Exception) else res.json()["choices"][0]["message"]["content"]
