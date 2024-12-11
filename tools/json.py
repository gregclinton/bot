def meta():
    return {
        "description": "Process json string.",
        "parameters": {
            "properties": {
                "json": {
                    "type": "string",
                    "description": "The json string to be processed."
                }
            },
            "required": ["json"]
        }
    }

def run(args, thread):
    return args["json"]
