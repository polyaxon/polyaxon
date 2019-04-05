FROM polyaxon/polyaxon-npm-base

# This dockerfile is intended for dev only purposes
MAINTAINER mourad mourafiq <mourad@polyaxon.com>

RUN apt-get -y update && \
    apt-get -y install git && \
    apt-get -y install nginx && \
    apt-get -y install libldap2-dev libsasl2-dev


COPY requirements /requirements/
RUN pip3 install --no-cache-dir -r /requirements/requirements-test.txt

VOLUME /tmp/plx/repos
VOLUME /polyaxon
WORKDIR /polyaxon
COPY . /polyaxon
