---
title: "Building containers with custom dockerfile"
sub_link: "builds/building-containers-custom-dockerfile"
meta_title: "Building containers with custom dockerfile - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Building containers with custom dockerfile - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

In the previous tutorial we showed how to create the docker image `polyaxon/polyaxon-quick-start` using the init Dockerfile. 
In this tutorial we will show how to use a custom Dockerfile from a local folder or a remote repo.

> **Note**: You can build docker images outside of Polyaxon, or use your own system.

## Local repo Dockerfile

Using the `job` runtime, users can use Polyaxon to build docker images, there are a couple of build options and components provided.

First we need to clone the quick-start repo which has a `Dockerfile` and `requirements.txt`.
To build the image that we are using in this quick-start tutorial using the dockerfile in the repo:

```yaml
FROM tensorflow/tensorflow:2.2.0

LABEL maintainer="Polyaxon, Inc. <contact@polyaxon.com>"

WORKDIR /code

COPY requirements.txt /code

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY model.py /code
```

We need to adjust the polyaxonfile to handle the uploads folder:

```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon/polyaxon-quick-start
  context:
    value: "{{ globals.run_artifacts_path }}/uploads"
hubRef: kaniko
```

The `hubRef` is the reference of the component we are going to run, in this case, it's a Kaniko component for building the image. 
We are also passing a parameter `destination` which is of type [image](/docs/core/specification/types/),
it defines the name of the image and the connection to use for pushing the image.
The [docker-connection](/docs/setup/connections/registry/) is a [connection](/docs/setup/connections/)
that we configured to authenticate Kaniko to push images.


You amy notice that the difference between this polyaxonfile and the previous polyaxonfile is that we are passing a context value to point to where Kaniko should find the dockerfile.
In our case it should look at the root of the uploads folder.


## Remote repo Dockerfile

Similar to the previous section, we can adjust our polyaxonfile to expect a Dockerfile coming from a remote repo:


```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon/polyaxon-quick-start
  context:
    value: "{{ globals.artifacts_path }}/polyaxon-quick-start"
runPatch:
  init:
    - git:
        url: "https://github.com/org/polyaxon/polyaxon-quick-start"
hubRef: kaniko
```

You can notice that the context value is now pointing to where the repo is being cloned using the git initializer.
