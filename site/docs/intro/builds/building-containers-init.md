---
title: "Building containers with the init section"
sub_link: "builds/building-containers-init"
meta_title: "Building containers with the init section - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Building containers with the init section - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

During this quick-start tutorial, we have been using a docker image `polyaxon/polyaxon-quick-start`,
which was built using a Polyaxonfile as well.

> **Note**: You can build docker images outside of Polyaxon, or use your own system.

## Docker images

Using the `job` runtime, users can use Polyaxon to build docker images, there are a couple of build options and components provided.

For example the image we are using in this tutorial is based on this Polyaxonfile:

```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon/polyaxon-quick-start
runPatch:
  init:
  - dockerfile:
      image: "tensorflow/tensorflow:2.0.1-py3"
      run:
      - 'pip3 install --no-cache-dir -U polyaxon'
      langEnv: 'en_US.UTF-8'
hubRef: kaniko
```

This configuration is using a public component called Kaniko,
it uses an initializer [dockerfile](/docs/core/specification/init/) which generates simple dockerfile.

> **Note**: We could have created a dockerfile, and used a git initializer to clone the repo containing the dockerfile.

Since we do not want to create or modify the Kaniko component,
we are using the `runPatch` section to add the init section to the job.
The `runPatch` allows us to patch the component definition without having to rewrite it from scratch,
in this case, we are generating a dockerfile.
The dockerfile we are generating is a based on a tensorflow docker image and
we are just installing `polyaxon` library and some extra dependencies to use with the [tracking module](/docs/experimentation/tracking/).

The `hubRef` is the reference of the component we are going to run, in this case, it's a Kaniko component for building the image.

We are also passing a parameter `destination` which is of type [image](/docs/core/specification/types/),
it defines the name of the image and the connection to use for pushing the image.
The [docker-connection](/docs/setup/connections/registry/) is a [connection](/docs/setup/connections/)
that we configured to authenticate Kaniko to push images.
