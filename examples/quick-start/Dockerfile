FROM tensorflow/tensorflow:2.2.0

# This dockerfile emulate the behavior of Polyaxon v0 using similar tricks for leverage the build cache
LABEL maintainer="Polyaxon, Inc. <contact@polyaxon.com>"

WORKDIR /code

COPY requirements.txt /code

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY model.py /code
