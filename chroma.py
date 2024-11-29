import chromadb
from chromadb.utils import embedding_functions
import llm
import os
import json

client = chromadb.PersistentClient(path="./chroma/Sephora")
# client.delete_collection("product_catalog"); exit()

def collection(name):
    return client.get_or_create_collection(
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

def invoke(query):
    collections = ", ".join(map(lambda collection:  collection.name, client.list_collections()))
    o = json.loads(llm.invoke(input_instruction.replace("{collections}", collections), query))
    return collection(o["database"]).query(query_texts=[o["search"]], n_results=1)["documents"][0][0]

print(invoke("do you sell men's hats"))

if False:
    documents = []
    metadatas = []
    ids = []
    id = 10000

    for shoppers in ["men", "women"]:
        instruction = "Yor are a creative catalog writer."
        for product in ["hats", "shirts", "pants", "shoes"]:
            prompt = f"Invent a catlog description (about 200 words) and price for {shoppers}'s {product}. Pure text format, no markdown."
            documents.append(llm.invoke(instruction, prompt))
            metadatas.append({"section": f"{shoppers}'s {product}"})
            ids.append(f"id-{id}")
            id += 1

    def create(name, documents, metadatas, ids):
        collection(name).add(documents=documents, metadatas=metadatas, ids=ids)