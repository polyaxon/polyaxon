FROM polyaxon-base-dev

# This dockerfile is intended for dev only purposes
LABEL maintainer="Polyaxon, Inc. <contact@polyaxon.com>"

RUN apt-get -y update && \
    apt-get -y install nginx && \
    apt-get -y install libldap2-dev libsasl2-dev && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

COPY /platform/coreapi/requirements /requirements/
RUN pip3 install --no-cache-dir -r /requirements/requirements-dev.txt

VOLUME /polyaxon
COPY /core /polyaxon/core
COPY /traceml /polyaxon/traceml
COPY /hypertune /polyaxon/hypertune
COPY /datatile /polyaxon/datatile
COPY /platform /polyaxon/platform
WORKDIR /polyaxon

ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/sdks/python/http_client/v1"
ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/traceml"
ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/hypertune"
ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/datatile"
ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/core"
ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/platform/polycommon"
ENV PYTHONPATH="${PYTHONPATH}:/polyaxon/platform/coredb"
RUN pip3 install -e /polyaxon/core

WORKDIR /polyaxon/platform/coreapi
