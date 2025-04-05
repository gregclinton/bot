
async def run(model: str, provider: str, thread: dict):
    "Change your llm model and provider."
    thread[model] = model
    thread[provider] = provider
    for message in thread["messages"]:
        if message["role"] == "assistant":
            for key in ["refusal", "annotations"]:
                message.pop(key, None)

    return f"Now using {provider}'s {model}."