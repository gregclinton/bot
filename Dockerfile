# docker build -t bot .
# docker rm hal
# sudo docker run --network home --name hal -it -p 443:443 bot:latest bash

FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl
RUN pip install fastapi uvicorn requests boilerpy3 chromadb python-multipart
COPY ./*.py /root
COPY ./tools /root/tools
COPY ./docs /root/docs
COPY ./client /root/client
COPY ./up /root
RUN apt install -y nano