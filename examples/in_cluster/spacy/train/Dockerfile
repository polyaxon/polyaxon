FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANGUAGE n_US.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR off

# Install git and g++
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ca-certificates \
    g++ \
    gcc \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Upgrade to latest pip
RUN pip install --upgrade pip

# Install latest spacy and download english model
RUN pip install spacy

# Change model to language of choice: https://spacy.io/usage/models
RUN python -m spacy download en_core_web_sm

# Polyaxon

RUN pip install polyaxon

WORKDIR /code
COPY build /code
