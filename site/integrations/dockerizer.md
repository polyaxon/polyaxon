---
title: "Dockerizer"
meta_title: "Native Docker Builder"
meta_description: "Polyaxon allows users to build container images using the native builder project."
custom_excerpt: "Polyaxon native builder is a Python library for building container using the Docker Engine API."
image: "../../content/images/integrations/native-builder.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - containers
featured: false
popularity: 1
visibility: public
status: published
---

Polyaxon allows users to build container images using a native builder.

## Overview

Polyaxon provides a simple component for building containers with a native builder, you can check the [component on Polyaxon](https://cloud.polyaxon.com/ui/polyaxon/dockerizer/versions) for more details.

All versions of this component expect a `destination`; this is the `image:tag` that the component will push the image to.
Since, you will need to provide auth and other information to resolve the registry, 
you will generally need to pass a connection with the destination value:

```yaml
params:
  destination:
    connection: CONNECTION_NAME
    value: "image:tag"
```

You can additionally customize some other aspects about this built-in component:
 * context: default is `{{ globals.artifacts_path }}`
 * nocache: default is `false`
 
Please see the [component's definition](https://cloud.polyaxon.com/ui/polyaxon/dockerizer/components/latest) for more details about the implementation.

## Setting a registry connection

Before you can use this component, you need to make sure to declare a registry connection in your connections catalog.

Please read this introduction to [registry connections](/docs/setup/connections/registry/) to understand the process, and this list of [registry integrations](/integrations/registries/) that you can use.

## Creating containers 

### Using an init `dockerfile`

```yaml
version: 1
kind: operation
params:
  destination:
    connection: CONNECTION_NAME
    value: image:tag
runPatch:
  init:
  - dockerfile:
      image: "tensorflow/tensorflow:2.0.1-py3"
      run:
      - 'pip3 install --no-cache-dir -U polyaxon'
      langEnv: 'en_US.UTF-8'
hubRef: dockerizer
```

This operation will initialize a dockerfile automatically under `{{ globals.artifacts_path }}/Dockerfile`, and `Dockerizer` component will build that dockerfile and push it.

### Using a custom dockerfile from a local folder

Assuming you have this local folder structure:

```
local-repo
└──Dockerfile
└──file1
└──file2
└──folder1
    ├──...
    └──file1
    └──file2
```

You can create an operation that expects code to be uploaded:

```bash
polyaxon run -f operation.yaml -u [-p]
```

The operation should look like this:

```yaml
version: 1.1
kind: operation
params:
  destination:
    connection: CONNECTION_NAME
    value: image:tag
  context:
    value: "{{ globals.run_artifacts_path }}/uploads"
hubRef: dockerizer
```

Since we are setting the context to the uploads path, `Dockerizer` will look for any file called `Dockerfile` under that path, which should be populated with the uploaded code from local machine.

### Using a custom dockerfile from a git repo

Assuming you have this folder structure in your repo:

```
repo
└──Dockerfile
└──file1
└──file2
└──folder1
    ├──...
    └──file1
    └──file2
```

You can create an operation that expects an git initializer

```bash
polyaxon run -f operation.yaml -u [-p]
```

The operation should look like this:

```yaml
version: 1.1
kind: operation
params:
  destination:
    connection: CONNECTION_NAME
    value: image:tag
  context:
    value: "{{ globals.artifacts_path }}/repo-name"
runPatch:
  init:
    - git:
        url: "https://github.com/org/repo-name"
hubRef: dockerizer
```

Since we are setting the context to the match where the repo will be initialized, 
`Dockerizer` will look for any file called `Dockerfile` under that path, which should be populated with the code from git repo.

## Queues, presets, node scheduling, custom resources, ... 

You can customize the queue, presets, environment section, node selector, connections, initializers, resources requirements, ...

```yaml
version: 1.1
kind: operation
params:
  destination:
    connection: CONNECTION_NAME
    value: image:tag
hubRef: dockerizer
queue: agent-name/queue-name
presets: [preset1, preset2]
runPatch:
  connections: [...]
  environment:
    ...
  container:
    resources:
      requests:
        memory: 300Mi
``` 

## Forking and customizing the component

If you need to expose the `dockerizer` component with your predefined configuration,
we suggest that you clone the [component](https://cloud.polyaxon.com/ui/polyaxon/dockerizer/components/latest) and customize it.

On Polyaxon CE, you will need to create a new `.yaml` file where you will host the content of the component, and users can build container using:

 * `polyaxon run -f my-custom-dockerizer.yaml`
 * `polyaxon run --url https://path/to/my-custom-dockerizer.yaml` 

On Polyaxon Cloud or Polyaxon EE, you just need to add a new [component hub](/docs/management/component-hub/).
The end users will need to run with `org-name/dockerizer` instead of `dockerizer`:

```bash
polyaxon run --hub acme/dockerizer
```

> **Note**: In order to use `acme/dockerizer` without `:tag` you need to name the version `latest`.

## Versions

All `dockerizer` versions can be found on the [component hub](https://cloud.polyaxon.com/ui/polyaxon/dockerizer/components/).

You can also run:

```bash
polyaxon hub ls -c dockerizer
```

