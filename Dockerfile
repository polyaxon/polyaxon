FROM polyaxon/polyaxon-npm-base

MAINTAINER mourad mourafiq <mouradmourafiq@gmail.com>

RUN apt-get -y update && \
    apt-get -y install git && \
    apt-get -y install nginx


COPY requirements.txt /setup/
COPY requirements-dev.txt /setup/
COPY requirements-test.txt /setup/
RUN pip3 install --no-cache-dir -r /setup/requirements-test.txt

VOLUME /tmp/plx/repos
VOLUME /polyaxon
WORKDIR /polyaxon
COPY . /polyaxon

RUN rm -f /etc/nginx/sites-enabled/default
COPY web/nginx.conf /etc/nginx/sites-enabled/polyaxon.conf
COPY web/uwsgi_params /etc/nginx/uwsgi_params
