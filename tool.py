from importlib import import_module
import inspect
import os
import sys
import builtins

def module_names(thread):
    for name in (thread["use"]["tools"] if thread.get("use") else builtins.open("tools/use").read()).split(","):
        yield(f"tools.{name}")

def modules(thread):
    for name in module_names(thread):
        yield import_module(name)

def reset(thread):
    for module in modules(thread):
        if hasattr(module, "reset"):
            module.reset(thread)
    return thread

def open(thread):
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
    } for module in modules(thread)]

def run(name, args):
    return import_module(f"tools.{name}").run(**args)

def close(thread):
    [sys.modules.pop(name) for name in module_names(thread)]
