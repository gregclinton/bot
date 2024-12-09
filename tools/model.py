import os

def meta():
    return {
        "description": "Specify llm model and/or temperature.",
        "parameters": {
            "properties": {
                "model": {
                    "type": "string",
                    "description": "gpt-4o or gpt-4o-mini."
                },
                "temperature": {
                    "type": "integer",
                    "description": "0 to 100"
                }
            },
            "required": []
        }
    }

def run(args, thread):
    if args.get("model"):
        thread["model"] = args["model"]
    
    if args.get("temperature"):
        thread["temperature"] = args["temperature"] / 100.0
    return "success"
