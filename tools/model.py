import chat

async def run(model: str, provider: str, thread: dict):
    """
    Change your llm model and provider.
    Providers: openai, anthropic, azure, google, mistral, xai, fireworks, nvidia, together, groq, openrouter, deepinfra, nebius, taalas
    """
    print(f"{thread['assistant']}: model: {model}, {provider}", flush = True)
    chat.set_model(thread, provider, model)
    return f"Now using {provider}'s {model}."