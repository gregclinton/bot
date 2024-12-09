import os

def meta():
    return {
        "description": "Specify llm model and temperature.",
        "parameters": {
            "properties": {
                "model": {
                    "type": "string",
                    "description": "gpt-4o or gpt-4o-mini."
                },
                "temperature": {
                    "type": "string",
                    "description": "0 to 1"
                }
            },
            "required": ["model", "temperature"]
        }
    }

def run(args, thread):
    model, temperature = (args["model"], args["temperature"])
    thread["model"] = model
    thread["temperature"] = int(temperature)
    return "success"
