FROM polyaxon/polyaxon-npm-base

# This dockerfile is intended for dev only purposes
MAINTAINER mourad mourafiq <mourad@polyaxon.com>

# add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r polyaxon && useradd -r -m -g polyaxon polyaxon

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

RUN rm -f /etc/nginx/sites-enabled/default
RUN rm -f /etc/nginx/sites-available/default
RUN mkdir /etc/nginx/polyaxon
COPY web/nginx.conf /etc/nginx/sites-available/polyaxon.config
RUN ln -s /etc/nginx/sites-available/polyaxon.config /etc/nginx/sites-enabled/polyaxon.conf
COPY web/uwsgi_params /etc/nginx/uwsgi_params
