FROM polyaxon/polyaxon:api-cpu-3-130

MAINTAINER mourad mourafiq <mouradmourafiq@gmail.com>

RUN apt-get -y update && \
    apt-get -y install curl git

# copy requirements.txt
COPY requirements.txt /setup/
COPY requirements-dev.txt /setup/
COPY requirements-test.txt /setup/
RUN pip3 install --no-cache-dir -r /setup/requirements-test.txt

VOLUME /polyaxon
WORKDIR /polyaxon
copy . /polyaxon

CMD uwsgi --ini uwsgi.ini
