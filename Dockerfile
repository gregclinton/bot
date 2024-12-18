FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl nano

RUN pip install fastapi uvicorn requests boilerpy3 chromadb python-multipart

WORKDIR /root

RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=example.com"

COPY . .

RUN rm Dockerfile .gitignore again
