# https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#retriever

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv

load_dotenv('keys')

def create_db():
    import os
    os.environ["USER_AGENT"] = "simon"
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    docs = [WebBaseLoader(f"https://lilianweng.github.io/posts/{path}/").load() for path in [
        "2023-06-23-agent",
        "2023-03-15-prompt-engineering",
        "2023-10-25-adv-attack-llm",
    ]]

    splits = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = 100, chunk_overlap = 50
    ).split_documents([item for sublist in docs for item in sublist])

    Chroma.from_documents(
        documents = splits,
        collection_name = "rag-chroma",
        embedding = OpenAIEmbeddings(),
        persist_directory = 'storage'
    )

# create_db()

retriever = create_retriever_tool(Chroma(
        collection_name = "rag-chroma",
        embedding_function = OpenAIEmbeddings(),
        persist_directory = 'storage'
    ).as_retriever(),
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
)

tools = [retriever]