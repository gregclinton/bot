from importlib import import_module
import inspect
import os
import sys
import builtins

def module_names():
    for name in builtins.open("tools/use").read().split(","):
        yield(f"tools.{name}")

def modules():
    for name in module_names():
        yield import_module(name)

def reset(thread):
    thread["tools"] = tools = thread.get("tools", {})

    for module in modules():
        if hasattr(module, "reset"):
            name = module.__name__[6:] # strip "tools." 
            tools[name] = data = tools.get(name, {})
            module.reset(data)
    return thread

def open():
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
    } for module in modules()]

def run(name, args):
    return import_module(f"tools.{name}").run(**args)

def close():
    [sys.modules.pop(name) for name in module_names()]
