import chromadb
import json
import logging
import llm

path = "chroma"

def run(collection: str, search: str, thread: dict):
    "Searches the given chromadb collection using the given search string."
    client = chromadb.PersistentClient(path=path)
    collections = [collection.name for collection in client.list_collections()

    if collection in collections:
        collection = client.get_collection(collection)

        text = f"Chromadb search results:\n\n\n"

        for doc in collection.query(query_texts=search, n_results=3)["documents"][0]:
            text += llm.mini(f"Context:\n{doc}\n\n\nQuery:\n{search}\nAnswer:\n") + "\n\n\n"

        return llm.mini(text + f"Summarize the above various search results:\n")
    else:
        return f"The collection \"{collection}\" was not found. Our collections include: " + ", ".join(collections)

logging.getLogger('chromadb').setLevel(logging.ERROR)

def create_collection(collection, prompt):
    return
    documents = json.loads(llm.mini(prompt))
    ids = [str(i) for i in range(10000, 10000 + len(documents))]
    chromadb.PersistentClient(path=path).get_or_create_collection(name=collection).add(documents=documents, ids=ids)

create_collection("giovanni", """
Output a raw JSON array of 20 strings, not objects, without markdown or comments,
each being a pizza choice with wonderful description and price
at Giovanni's, a fictious Chicago pizzeria.
""")

# chromadb.PersistentClient(path=path).delete_collection("medicare")