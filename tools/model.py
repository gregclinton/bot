import os

def invoke(text, thread):
    model, temperature = (s.strip() for s in (text.split(",") + ["0"])[:2])
    thread["model"] = model
    thread["temperature"] = int(temperature)
    return "success"
