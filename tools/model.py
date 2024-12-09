import os

def descriptions():
    return (
        "Specify llm model and temperature.",
        "model,temperature: Model can be gpt-4o or gpt-4o-mini. Temperature is from 0 to 100."
    )
def run(text, thread):
    model, temperature = (s.strip() for s in (text.split(",") + ["0"])[:2])
    thread["model"] = model
    thread["temperature"] = int(temperature)
    return "success"
