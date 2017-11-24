FROM polyaxon/polyaxon-base

MAINTAINER mourad mourafiq <mouradmourafiq@gmail.com>

COPY requirements.txt /setup/
RUN pip3 install --no-cache-dir -r /setup/requirements.txt

VOLUME /polyaxon
WORKDIR /polyaxon
copy . /polyaxon
