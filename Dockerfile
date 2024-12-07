# docker build -t bot .

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends wget curl && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN pip install fastapi uvicorn python-dotenv requests chromadb openai matplotlib