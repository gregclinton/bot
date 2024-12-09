import chromadb
from chromadb.utils import embedding_functions
import llm
import os
import json
import logging

def meta():
    return {
        "description": "Probe a chromedb database.",
        "parameters": {
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to be run."
                }
            },
            "required": ["query"]
        }
    }

def run(args, thread):
    collections = ", ".join(map(lambda collection:  collection.name, client.list_collections()))

    if collections:
        msg = lambda role, content: { "role": role, "content": content }
        ask = lambda instruction, prompt: llm.invoke([msg("system", instruction), msg("user", args["query"])])

        o = json.loads(ask("""
Currently our chromadb installation has the following collections: {collections}
From the user prompt generate the most appropriate collection and search to use.
Output JSON object with collection key, a string, and search key, also a string.
Output the raw JSON without markdown.
""".replace("{collections}", collections), question))

        results = " ".join(collection(o["collection"]).query(query_texts=[o["search"]], n_results=1)["documents"][0])
        answer = ask("Given the context, answer the question.", f"Context: {results}\n\nQuestion: {question}\n\nAnswer: ")

        return answer
    else:
        return "No databases available."

logging.getLogger('chromadb').setLevel(logging.ERROR)

client = chromadb.PersistentClient(path=f"chroma")

def collection(name):
    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

def delete_collection(name):
    client.delete_collection(name)

def create_collection_from_huge_text(name, text):
    chunk_size = 2000
    overlap = 100
    chunking = range(0, len(text), chunk_size - overlap)
    documents = [text[i : i + chunk_size] for i in chunking]
    metadatas = [{"id": i} for i in chunking]
    ids = [str(i) for i in chunking]
    collection(name).add(documents=documents, metadatas=metadatas, ids=ids)

def create_collection_from_files_in_answer_folder(name):
    documents = []
    metadatas = []
    ids = []

    i = 100000

    for file in filter(os.path.isfile, map(lambda f: os.path.join(f"answers/{name}/", f), os.listdir(f"answers/{name}/"))):
         documents.append(open(file, "r").read())
         metadatas.append({ "source": os.path.basename(file) })
         ids.append(str(i))
         i += 1

    collection(name).add(documents=documents, metadatas=metadatas, ids=ids)

# create_collection_from_files_in_answer_folder("Medicare")