# docker build -t gregclinton/hal .
# docker login -u gregclinton
# docker push gregclinton/hal

FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl unzip
RUN pip install fastapi uvicorn
WORKDIR /root
COPY start .
CMD ["sh", "start"]
