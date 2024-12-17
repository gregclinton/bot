# docker build -t bot .
# docker rm hal
# sudo docker run --network home --name hal -it -p 443:443 bot:latest bash
# sudo docker run --network home --name mal -it bot:latest bash

FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl nano && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn requests boilerpy3 chromadb python-multipart

COPY . /root
WORKDIR /root
