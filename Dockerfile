# docker build -t bot .
# sudo docker run -p 443:443 -d --network home --name hal bot:latest bash up
# docker exec hal echo -n ",model" >> tools/use
# docker logs hal
# curl -k https://localhost
# curl -k -X POST https://localhost/bot/threads
# docker rm -f hal

FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl nano

RUN pip install fastapi uvicorn requests boilerpy3 chromadb python-multipart

WORKDIR /root

RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=example.com"

COPY . .

RUN . ./secrets

RUN rm secrets Dockerfile .gitignore
