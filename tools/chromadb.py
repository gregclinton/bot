import chromadb
import json
import logging
import llm

def run(collection: str, search: str, thread: dict):
    "Searches the given chromadb collection using the given search string."
    client = chromadb.PersistentClient(path="chroma")
    collections = [collection.name for collection in client.list_collections()]

    if collection in collections:
        collection = client.get_or_create_collection(name=collection)

        text = f"Mish-mash of chromadb search results:\n\n\n"
        text += " ".join(collection.query(query_texts=search, n_results=3)["documents"][0])

        return llm.mini(text + f"\n\n\nQuery:\n{search}\nAnswer:\n")
    else:
        return f"The collection \"{collection}\" was not found. Our collections include: " + ", ".join(collections)

logging.getLogger('chromadb').setLevel(logging.ERROR)

def create_collection(collection, prompt):
    return
    documents = json.loads(llm.mini(prompt))
    ids = [str(i) for i in range(10000, 10000 + len(documents))]
    chromadb.PersistentClient(path="chroma").get_or_create_collection(name=collection).add(documents=documents, ids=ids)

create_collection("giovanni", """
Output a raw JSON array of 20 strings, not objects, without markdown or comments,
each being a pizza choice with wonderful description and price
at Giovanni's, a fictious Chicago pizzeria.
""")

# chromadb.PersistentClient(path="chroma").delete_collection("medicare")