# docker build -t bot .

# FROM python:3.11-slim
# RUN apt-get update && apt-get install -y curl
# RUN pip install fastapi uvicorn python-dotenv requests boilerpy3 python-multipart chromadb

# docker build -t alpine .

FROM python:3-alpine
RUN apk add py3-pip
RUN pip install fastapi uvicorn python-dotenv requests boilerpy3 python-multipart
