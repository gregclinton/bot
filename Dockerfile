# docker build -t agent .

FROM ubuntu:24.04

RUN apt update && apt upgrade -y && \
    apt install -y software-properties-common wget curl && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update && \
    apt install -y python3.11 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 

RUN pip install langgraph langsmith langchain-core langchain-community

RUN pip install langchain_openai langchain_anthropic

RUN pip install fastapi uvicorn

RUN pip install tavily_python

RUN pip install "langgraph-cli[inmem]==0.1.55"

RUN pip install beautifulsoup4

RUN pip install chromadb