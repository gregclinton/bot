# sudo openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=greg.com"
# docker network create home

case "$1" in
    proxy)
        sudo docker run --network home -p 443:443 -v `pwd`:/root -w /root bot:latest uvicorn proxy:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
        ;;
    up)
        sudo docker run --network home --name hal -p 8123:8123 -v `pwd`:/root -w /root bot:latest uvicorn hal:app --host 0.0.0.0 --port 8123
        ;;
    run)
        sudo docker run -v `pwd`:/root -w /root bot:latest python3 chat.py
        ;;
esac
