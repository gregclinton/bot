from importlib import import_module
import inspect

def modules(tools):
    for tool in tools:
        yield import_module(f"tools.{tool}")

def reset(tools, thread):
    for module in modules(tools):
        if hasattr(module, "reset"):
            module.reset(thread)
    return thread

def create(tools):
    return [{
        "type": "function",
        "function": {
            "name": module.__name__[6:],  # strip "tools."
            "description": module.run.__doc__,
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    param: {
                        "type": {"int": "integer", "str": "string"}[details.annotation.__name__],
                        "description": param
                    }
                    for param, details in inspect.signature(module.run).parameters.items()
                    if param != "thread"
                },
                "additionalProperties": False,
                "required": [
                    param for param in inspect.signature(module.run).parameters if param != "thread"
                ]
            }
        }
    } for module in modules(tools)]

def run(name, args):
    return import_module(f"tools.{name}").run(**args)