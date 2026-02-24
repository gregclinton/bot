import requests
import json
import os

def invoke():
    provider = "openai"
    model = "gpt-4.1-nano"
    messages = [{"role": "user", "content": "What is 2+2?"}]

    if provider == "fireworks":
        model = f"accounts/fireworks/models/{model}"

    data = {
        "model": model,
        "temperature": 0,
        "messages": messages,
    }

    if provider == "openai":
        if model.startswith("o"):
            del data["temperature"]
    elif provider == "anthropic":
        data["max_tokens"] = 1024

    content = None
    count = 0

    while not content and count < 10:
        count += 1

        res = requests.post(
            f"""https://{({
                "openai": "api.openai.com/v1",
                "anthropic": "api.anthropic.com/v1",
                "google": "generativelanguage.googleapis.com/v1beta/openai",
                "mistral": "api.mistral.ai/v1",
                "xai": "api.x.ai/v1",
                "fireworks": "api.fireworks.ai/inference/v1",
                "nvidia": "integrate.api.nvidia.com/v1",
                "together": "api.together.xyz/v1",
                "groq": "api.groq.com/openai/v1",
                "openrouter": "openrouter.ai/api/v1",
                "deepinfra": "api.deepinfra.com/v1/openai",
                "nebius": "api.studio.nebius.com/v1",
                "taalas": "api.taalas.com/v1",
            }[provider])}/chat/completions""",
            headers = {
                'Authorization': 'Bearer ' + os.environ.get(f"{provider.upper()}_API_KEY"),
                'Content-Type': 'application/json'
            },
            json = data
        )

        try:
            res.raise_for_status()
            message = res.json()["choices"][0]["message"]
            content = message.get("content")

        except Exception as e:
            content = str(e) + "\n" + res.text

    return content or "Could you rephrase that, please?"

    
print(invoke())