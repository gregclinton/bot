import chat

async def run(model: str, provider: str, thread: dict):
    "Change your llm model and provider."
    print(f"{thread["assistant"]}: model: {model}, {provider}")
    chat.set_model(thread, provider, model)
    return f"Now using {provider}'s {model}."