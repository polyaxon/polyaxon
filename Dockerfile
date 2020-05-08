FROM polyaxon/polyaxon-npm-base

# This dockerfile is intended for dev only purposes
LABEL maintainer="Polyaxon, Inc. <contact@polyaxon.com>"

RUN apt-get -y update && \
    apt-get -y install nginx && \
    apt-get -y install libldap2-dev libsasl2-dev && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements /requirements/
RUN pip3 install --no-cache-dir -r requirements/base.txt -r requirements/platform.txt

VOLUME /tmp/plx/repos
VOLUME /polyaxon
WORKDIR /polyaxon
COPY . /polyaxon
