FROM python:3.8-slim
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Bangkok
RUN apt-get update && apt-get install -y tzdata && apt-get install -yq --no-install-recommends \
    unzip \
    wget \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt
