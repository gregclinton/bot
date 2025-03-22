import requests
import os
import json
import tool

def invoke(thread):
    provider = thread["provider"]
    model = thread["model"]
    inference = None
    messages = thread["messages"]

    if provider == "huggingface":
        model, inference = model.split(",")
        if inference == "hf-inference":
            inference += "/models/" + model

    data = {
        "model": model,
        "temperature": 0,
        "messages": messages,
    }

    if provider == "anthropic":
        data["max_tokens"] = 1024

    if thread["tools"]:
        data["tools"] = thread["tools"]
        data["tool_choice"] = "auto"

    content = None
    count = 0

    while not content and count < 10:
        count += 1

        res = requests.post(
            url = {
                "openai": "https://api.openai.com/v1/chat/completions",
                "anthropic": "https://api.anthropic.com/v1/chat/completions",
                "google": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                "mistral": "https://api.mistral.ai/v1/chat/completions",
                "x": "https://api.x.ai/v1/chat/completions",
                "huggingface": f"https://router.huggingface.co/{inference}/v1/chat/completions",
                "fireworks": "https://api.fireworks.ai/inference/v1/chat/completions",
                "nvidia": "https://integrate.api.nvidia.com/v1/chat/completions",
                "together": "https://api.together.xyz/v1/chat/completions",
                "groq": "https://api.groq.com/openai/v1/chat/completions",
                "deepinfra": "https://api.deepinfra.com/v1/chat/completions",
            }[provider],
            headers = {
                'Authorization': 'Bearer ' + os.environ[f"{provider.upper()}_API_KEY"],
                'Content-Type': 'application/json'
            },
            json = data
        )

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

                if name != "consult":
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
            content = str(e) + "\n" + res.text

    return content or "Could you rephrase that, please?"