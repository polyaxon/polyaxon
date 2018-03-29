FROM polyaxon/polyaxon-npm-base

MAINTAINER mourad mourafiq <mouradmourafiq@gmail.com>

RUN apt-get -y update && \
    apt-get -y install git && \
    apt-get -y install nginx


COPY requirements/requirements-base.txt /requirements/
COPY requirements/requirements.txt /requirements/
COPY requirements/requirements-dev.txt /requirements/
COPY requirements/requirements-test.txt /requirements/
RUN pip3 install --no-cache-dir -r /requirements/requirements-test.txt

VOLUME /tmp/plx/repos
VOLUME /polyaxon
WORKDIR /polyaxon
COPY . /polyaxon

RUN rm -f /etc/nginx/sites-enabled/default
RUN rm -f /etc/nginx/sites-available/default
COPY web/nginx_local.conf /etc/nginx/sites-available/polyaxon.config
RUN ln -s /etc/nginx/sites-available/polyaxon.config /etc/nginx/sites-enabled/polyaxon.conf
COPY web/uwsgi_params /etc/nginx/uwsgi_params
