import chromadb
from chromadb.utils import embedding_functions
import llm
import os
import json

def client(company):
    return chromadb.PersistentClient(path=f"./chroma/{company}")

def collection(company, name):
    return client(company).get_or_create_collection(
        name=name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

input_instruction = """
Currently we have the following databases: {collections}

From the user prompt generate the most appropriate database and search to use.

Output JSON object with database and search fields as raw JSON string without markdown.
"""

def invoke(company, query):
    collections = ", ".join(map(lambda collection:  collection.name, client(company).list_collections()))
    o = json.loads(llm.invoke(input_instruction.replace("{collections}", collections), query))
    collection_name = o["database"]
    search = o["search"]["category"]
    results = collection(company, collection_name).query(query_texts=[search], n_results=1)["documents"][0][0]
    return f"Our search of the {collection} database yields the following result: \n{results}"

if False:
    documents = []
    metadatas = []
    ids = []
    id = 10000

    for shoppers in ["men", "women"]:
        instruction = "Yor are a creative catalog writer."
        for product in ["hats", "shirts", "pants", "shoes"]:
            prompt = f"Invent a catlog description (about 200 words) and price for {shoppers}'s {product}. Pure text format, no markdown."
            print(f"{shoppers} {product}", flush=True)
            documents.append(llm.invoke(instruction, prompt))
            metadatas.append({"section": f"{shoppers}'s {product}"})
            ids.append(f"id-{id}")
            id += 1

    collection("Sephora", "catalog").add(documents=documents, metadatas=metadatas, ids=ids)

# client.delete_collection("product_catalog"); exit()
