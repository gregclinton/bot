# docker build -t gregclinton/hal .
# docker login -u gregclinton
# docker push gregclinton/hal
# https://docs.runpod.io/pods/configuration/expose-ports
# https://hr2ht4crrki63o-4000.proxy.runpod.net

FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl nano git-core openssh-server
RUN pip install fastapi uvicorn requests httpx python-multipart
WORKDIR /root
COPY start .
CMD ["sh", "start"]
