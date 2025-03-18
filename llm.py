import requests
import os
import json
import tool

def from_model(model):
    provider = (
        "openai" if model.startswith("gpt")
        else "anthropic" if model.startswith("claude")
        else "google" if model.startswith("gemini")
        else "huggingface" if "/" in model
        else "groq"
    )
    url = {
        "openai": f"https://api.openai.com/v1/chat/completions",
        "huggingface": f"https://api-inference.huggingface.co/models/{model}",
        "groq": f"https://api.groq.com/openai/v1/chat/completions"
    }.get(provider)

    return url, os.environ[f"{provider.upper()}_API_KEY"]

def invoke(thread):
    content = None
    count = 0
    messages = thread["messages"]
    model = thread["model"]
    url, key = from_model(model)

    while not content and count < 10:
        count += 1
        res = requests.post(
            url,
            headers = {
                'Authorization': f"Bearer {key}",
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
            content = str(e) + "\n" + res.content

    return content or "Could you rephrase that, please?"