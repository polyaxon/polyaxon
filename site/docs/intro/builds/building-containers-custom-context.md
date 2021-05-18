---
title: "Building containers with custom context"
sub_link: "builds/building-containers-custom-context"
meta_title: "Building containers with custom context - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Building containers with custom context - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

> **Note**: Requires Polyaxon v1.9.1 or higher.

## Overview

In the previous tutorials we showed how to create the docker image `polyaxon/polyaxon-quick-start` using an init Dockerfile or using a custom Dockerfile.
In both cases the file that we used to start the build was named `Dockerfile`, the file was also saved under the same folder as the build context.
In this tutorial we will show how to use a custom file that does not need to be named `Dockerfile` and a different path under the context.

## Passing the dockerfile argument to Kaniko

The `Kaniko` component can accept an additional argument `dockerfile` which is the path to the dockerfile to be built, the default value is "Dockerfile".

Let's take the following example:

```
repo
└──other-dirs
    └──...
└──context 
    ├──...
    ├──polyaxonfiles
    │      ├──build.yml
    │      └──run.yml
    ├──...
    └──dockerfiles
           ├──Dockerfile.1
           └──Dockerfile.2
```

## Local repo 

In order to trigger 2 builds based on on `Dockerfile.1` and `Dockerfile.2` and only consider the paths under context:

 * Operation 1:

```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: IMAGE
  context:
    value: "{{ globals.run_artifacts_path }}/uploads/context"
  dockerfile:
    value: "dockerfiles/Dockerfile.1"
hubRef: kaniko
```

 * Operation 2:

```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon/polyaxon-quick-start
  context:
    value: "{{ globals.run_artifacts_path }}/uploads/context"
  dockerfile:
    value: "dockerfiles/Dockerfile.2"
hubRef: kaniko
```

The `hubRef` is the reference of the component we are going to run, in this case, it's a Kaniko component for building the image. 
We are also passing a parameter `destination` which is of type [image](/docs/core/specification/types/),
it defines the name of the image and the connection to use for pushing the image.
The [docker-connection](/docs/setup/connections/registry/) is a [connection](/docs/setup/connections/)
that we configured to authenticate Kaniko to push images.

In this example we are also specifying a relative path to the dockerfile to use. 

## Remote repo

Similar to the previous section, we can adjust our polyaxonfile to expect a Dockerfile coming from a remote repo:

 * Operation 1:

```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon/polyaxon-quick-start
  context:
    value: "{{ globals.artifacts_path }}/polyaxon-quick-start/context"
  dockerfile:
    value: "dockerfiles/Dockerfile.1"
runPatch:
  init:
    - git:
        url: "https://github.com/org/polyaxon/polyaxon-quick-start"
hubRef: kaniko
```

 * Operation 2:

```yaml
version: 1
kind: operation
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon/polyaxon-quick-start
  context:
    value: "{{ globals.artifacts_path }}/polyaxon-quick-start/context"
  dockerfile:
    value: "dockerfiles/Dockerfile.2"
runPatch:
  init:
    - git:
        url: "https://github.com/org/polyaxon/polyaxon-quick-start"
hubRef: kaniko
```
