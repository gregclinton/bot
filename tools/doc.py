import os

def meta():
    return {
        "description": "Read a document.",
        "parameters": {
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The document name."
                }
            },
            "required": ["name"]
        }
    }

def run(args, thread):
    output = ""
    doc =  args["name"].lower()
    if os.path.isfile(f"docs/{doc}"):
        docs = thread["docs"]
        docs.append(doc) if doc not in docs else None
        result = "successfully added"
    else:
        result = "not found"
    output += f"The {doc} doc was {result}.\n"
    return output
