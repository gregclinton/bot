import chromadb
from chromadb.utils import embedding_functions
import llm
import os
import json

def client(path):
    return chromadb.PersistentClient(path=f"chroma/{path}")

def collection(path, name):
    return client(path).get_or_create_collection(
        name=name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

def delete_collection(path, name):
    client(path).delete_collection(name)

def invoke(args):
    input_instruction = """
Currently we have the following databases: {collections}
From the user prompt generate the most appropriate database and search to use.
Output JSON object with database key, a string, and search key, also a string.
Output the raw JSON without markdown.
"""
    collections = ", ".join(map(lambda collection:  collection.name, client(args["path"]).list_collections()))

    if collections:
        o = json.loads(llm.invoke([
            { "role": "system", "content": input_instruction.replace("{collections}", collections)},
            { "role": "user", "content": args["search"]}
        ])["content"])
        collection_name = o["database"]
        search = o["search"]
        results = " ".join(collection(args["path"], collection_name).query(query_texts=[search], n_results=4)["documents"][0])
        return f"Our search of the {collection_name} database yielded the following result: \n{results}"
    else:
        return "As of yet, we have no databases."

def create_collection_from_huge_text(path, name, text):
    chunk_size = 2000
    overlap = 100
    chunking = range(0, len(text), chunk_size - overlap)
    documents = [text[i : i + chunk_size] for i in chunking]
    metadatas = [{"id": i} for i in chunking]
    ids = [str(i) for i in chunking]
    collection(path, name).add(documents=documents, metadatas=metadatas, ids=ids)

def create_answers_collection(path):
    documents = []
    metadatas = []
    ids = []

    i = 100000

    for file in filter(os.path.isfile, map(lambda f: os.path.join(f"answers/{path}/", f), os.listdir(f"answers/{path}/"))):
         documents.append(open(file, "r").read())
         metadatas.append(os.path.basename(file))
         ids.append(str(i))
         i += 1

    collection(path, "answers").add(documents=documents, metadatas=metadatas, ids=ids)
