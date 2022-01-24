FROM polyaxon/polyaxon-npm-base

# This dockerfile is intended for dev only purposes
LABEL maintainer="Polyaxon, Inc. <contact@polyaxon.com>"

COPY platform/base/requirements /base/requirements/
COPY core/requirements/requirements.txt /base/requirements/base.txt
COPY requirements/core.txt /base/requirements/core.txt
COPY requirements/test.txt /base/requirements/test.txt
RUN pip3 install --no-cache-dir -r /base/requirements/core.txt
RUN pip3 install --no-cache-dir -r /base/requirements/test.txt
RUN pip3 install --no-cache-dir -r /base/requirements/master.txt
RUN pip3 install --no-cache-dir -r /base/requirements/requirements-test.txt
RUN rm -rf /base
