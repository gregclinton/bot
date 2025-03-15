# https://platform.openai.com/docs/api-reference/chat

import requests
import os
import json
import tool

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
    bench = tool.create(thread)
    messages = thread["messages"]
    model = "llama-3.1-8b-instant"
    model = "qwen-qwq-32b"
    model = "gpt-4o-mini"

    if os.path.exists("notes"):
        messages[0]["content"] = open("notes").read()
    else:
        messages[0]["content"] = """
Keep things you don't want to forget in the notes file in your current working directory.
You can edit these notes with the shell tool.
These notes will comprise your system message.
"""
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