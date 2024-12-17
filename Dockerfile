# docker build -t bot .
# docker rm hal
# sudo docker run --network home --name hal -p 443:443 -d bot:latest
# sudo docker exec hal echo abc

FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl nano openssh-server

RUN pip install fastapi uvicorn requests boilerpy3 chromadb python-multipart

RUN mkdir /var/run/sshd

WORKDIR /root

RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=example.com"

COPY . .

RUN . ./secrets

RUN rm secrets Dockerfile .gitignore

RUN uvicorn proxy:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem &

RUN uvicorn bot:app --host 0.0.0.0 --port 8123 &
