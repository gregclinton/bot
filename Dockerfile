# docker build -t bot .

FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl
RUN pip install fastapi uvicorn python-dotenv requests boilerpy3 chromadb