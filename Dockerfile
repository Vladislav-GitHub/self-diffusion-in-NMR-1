FROM pytorch/pytorch:latest

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /

COPY requirements.txt $WORKDIR

RUN apt-get update && apt-get clean -y

RUN pip install -U pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . $WORKDIR