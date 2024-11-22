# https://python.langchain.com/docs/integrations/vectorstores/chroma/
# https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#retriever

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

embedding = OpenAIEmbeddings()

def store(collection_name, text):
    from langchain.schema import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splits = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = 1000, chunk_overlap = 100
    ).split_documents([Document(text)])

    Chroma.from_documents(
        documents = splits,
        collection_name = collection_name,
        embedding = embedding,
        persist_directory = f"chroma/{collection_name}")

def retriever(collection_name, description = ""):
    return create_retriever_tool(
        Chroma(
            collection_name = collection_name,
            embedding_function = embedding,
            persist_directory = f"chroma/{collection_name}"
        ).as_retriever(),
        f"retrieve_{collection_name}",
        f"Retrieve information about {collection_name}. {description}")