def run(model: str, temperature: int, thread: dict):
    """
    Specify llm model and temperature.
    """
    thread["model"] = model
    thread["temperature"] = temperature / 100
    return "success"
