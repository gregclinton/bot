def meta():
    return {
        "description": "Process json string.",
        "params": {
            "json": {
                "type": "string",
                "description": "The json string to be processed."
            }
        }
    }

def run(args, thread):
    return args["json"]
