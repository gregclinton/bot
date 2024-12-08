import os

def run(docs, thread):
    docs = docs.split("\n")[0].strip()
    output = ""
    for doc in docs.split(","):
        doc =  doc.strip().lower()
        if os.path.isfile(f"docs/{doc}"):
            docs = thread["docs"]
            docs.append(doc) if doc not in docs else None
            result = "successfully added"
        else:
            result = "not found"
        output += f"The {doc} doc was {result}.\n"
    return output
