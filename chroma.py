import chromadb
from chromadb.utils import embedding_functions
import llm
import os
import json
import subprocess

def client(company):
    return chromadb.PersistentClient(path=f"chroma/{company}")

def collection(company, name):
    return client(company).get_or_create_collection(
        name=name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name="text-embedding-ada-002"
        )
    )

def delete_collection(company, name):
    client(company).delete_collection(name)

def invoke(company, query):
    input_instruction = """
Currently we have the following databases: {collections}
From the user prompt generate the most appropriate database and search to use.
Output JSON object with database key, a string, and search key, also a string.
Output the raw JSON without markdown.
"""
    collections = ", ".join(map(lambda collection:  collection.name, client(company).list_collections()))

    if not collections:
        return "As of yet, we have no databases."

    o = json.loads(llm.invoke(input_instruction.replace("{collections}", collections), query))
    collection_name = o["database"]
    search = o["search"]
    results = " ".join(collection(company, collection_name).query(query_texts=[search], n_results=4)["documents"][0])
    return f"Our search of the {collection_name} database yielded the following result: \n{results}"

def create_collection_from_huge_text(company, name, text):
    chunk_size = 2000
    overlap = 100
    chunking = range(0, len(text), chunk_size - overlap)
    documents = [text[i : i + chunk_size] for i in chunking]
    metadatas = [{"id": i} for i in chunking]
    ids = [str(i) for i in chunking]
    collection(company, name).add(documents=documents, metadatas=metadatas, ids=ids)

def create_collection_of_documents(company, name, documents):
    metadatas = [{"id": i} for i in len(documents)]
    ids = [str(i) for i in len(documents)]
    collection(company, name).add(documents=documents, metadatas=metadatas, ids=ids)

def create_answers_collection(company):
    create_collection_from_huge_text(company, "answers", open(f"answers/{company}/answers.txt").read())

if False:
    documents = []

    for shoppers in ["men", "women"]:
        instruction = "Yor are a creative catalog writer."
        for product in ["hats", "shirts", "pants", "shoes"]:
            prompt = f"Invent a catlog description (about 200 words) and price for {shoppers}'s {product}. Pure text format, no markdown."
            documents.append(llm.invoke(instruction, prompt))

    create_collection_of_documents("Sephora", "catalog", documents)

# create_answers_collection("Cox Cable")