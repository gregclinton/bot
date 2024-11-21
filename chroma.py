# https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#retriever

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

embedding = OpenAIEmbeddings()

def store(collection_name, documents):
    Chroma.from_documents(
        documents = documents,
        collection_name = collection_name,
        embedding = embedding,
        persist_directory = f"chroma/{collection_name}")

def retriever(collection_name, description):
    return create_retriever_tool(
        Chroma(
            collection_name = collection_name,
            embedding_function = embedding,
            persist_directory = f"chroma/{collection_name}"
        ).as_retriever(),
        f"retrieve_{collection_name}",
        f"Retrieve information about  {description}")