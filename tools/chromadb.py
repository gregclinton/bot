import chromadb
import llm
import json
import logging

def meta():
    return {
        "description": "Search a chromadb collection.",
        "parameters": {
            "properties": {
                "collection": {
                    "type": "string",
                    "description": "The collection to search, either giovanni, ezno, or luca."
                },
                "search": {
                    "type": "string",
                    "description": "Search related to user's question."
                }
            },
            "required": ["collection", "search"]
        }
    }

def run(args, thread):
    collection = chromadb.PersistentClient(path="chroma").get_or_create_collection(name=args["collection"])
    return " ".join(collection.query(query_texts=[args["search"]], n_results=3)["documents"][0])


logging.getLogger('chromadb').setLevel(logging.ERROR)

def create_collection(collection, prompt):
    return
    documents = json.loads(llm.invoke([{"role": "user", "content": prompt}]))
    ids = [str(i) for i in range(10000, 10000 + len(documents))]
    chromadb.PersistentClient(path="chroma").get_or_create_collection(name=collection).add(documents=documents, ids=ids)

create_collection("giovanni", """
Output a raw JSON array of 20 strings, not objects, without markdown or comments,
each being a pizza choice with wonderful description and price
at Giovanni's, a fictious Chicago pizzeria. 
""")

# chromadb.PersistentClient(path="chroma").delete_collection("Medicare")