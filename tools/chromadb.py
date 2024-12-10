import chromadb
import llm
import json
import logging

def meta():
    return {
        "description": "Search a chromedb collection.",
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

def create_collection(name, prompt):
    documents = json.loads(llm.invoke(prompt))
    ids = [str(i) for i in range(10000, 10000 + len(documents) + 1)]
    print(documents)
    # chromadb.PersistentClient(path="chroma").get_or_create_collection(name=args["collection"]).add(documents=documents, metadatas=metadatas, ids=ids)


create_collection("giovanni", """
Output a raw JSON array of 20 strings,
each being a pizza choice with wonderful description and price
at Giovanni's, a fictious Chicago pizzeria. 
""")

chromadb.PersistentClient(path="chroma").delete_collection("Medicare")