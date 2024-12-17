# docker build -t bot .
# sudo docker run --network home --name hal -d -p 443:443 bot sh up
# sudo docker run --network home --name dmv -d bot sh up
# docker exec hal sh -c 'echo "For DMV questions talk to this bot: https://dmv/bot" >> docs/bots'
# docker exec hal sh -c 'echo -n ",mytool" >> tools/use'
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

RUN rm Dockerfile .gitignore
