import requests
import json
import os

def invoke(provider, model, sys, user):
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
        json = {
            "model": model,
            "messages": [
                {"role": "system", "content": sys},
                {"role": "user", "content": user}
            ],
        }
    )

    try:
        res.raise_for_status()
        message = res.json()["choices"][0]["message"]
        return message.get("content")

    except Exception as e:
        return str(e) + "\n" + res.text