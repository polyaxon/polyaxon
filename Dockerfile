FROM polyaxon/polyaxon:cpu-3-121

MAINTAINER mourad mourafiq <mouradmourafiq@gmail.com>

# copy requirements.txt
COPY requirements.txt /setup/
COPY requirements_testing.txt /setup/
RUN pip3 install --no-cache-dir -r /setup/requirements_testing.txt

VOLUME /polyaxon
WORKDIR /polyaxon
copy . /polyaxon


# TensorBoard
EXPOSE 6006
# IPython
EXPOSE 8888
