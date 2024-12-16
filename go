# sudo openssl req -x509 -newkey rsa:4096 -keyout /etc/ssl/private/key.pem -out /etc/ssl/certs/cert.pem -days 365 -nodes -subj "/CN=greg.com"

case "$1" in
    proxy)
        sudo docker run -p 443:443 -v `pwd`:/root -w /root bot:latest uvicorn proxy:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
        ;;
    up)
        sudo docker run -p 8123:8123 -v `pwd`:/root -w /root bot:latest uvicorn serve:app --host 0.0.0.0 --port 8123
        ;;
    run)
        sudo docker run -v `pwd`:/root -w /root bot:latest python3 chat.py
        ;;
esac
