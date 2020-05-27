---
title: "Horovod"
meta_title: "Horovod"
meta_description: "Polyaxon allows to schedule distributed Horovod experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "Horovod is a distributed training framework for TensorFlow, Keras, PyTorch, and MXNet. The goal of Horovod is to make distributed Deep Learning fast and easy to use."
image: "../../content/images/integrations/horovod.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - distributed-training
  - tracking
  - scheduling
featured: false
visibility: public
status: beta
---

Polyaxon allows to schedule distributed Horovod experiments, and supports tracking metrics, outputs, and models.

## Overview

By default polyaxon creates a master job, so you only need to provide the workers.

To enable distributed runs, you need to set the `framework` field to `horovod` and update the `environment` section.

The environment section allows to customize the resources of the master job, as well as defining the topology/replicas of the experiment with a specific definition for each framework.

To customize the master resources, you just need to define the resources in the environment section, e.g.

```yaml
...
framework: horovod
...
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      requests: 1
      limits: 1
```

## Define the distributed topology

[Distributed Horovod](https://github.com/horovod/horovod#running-horovod) defines a master task (worker with rank 0) and a set of worker tasks.

To define a Horovod cluster in Polyaxon with a master, 3 workers,
add a replicas subsection to the environment section of your polyaxonfile:


```yaml
...
framework: horovod
...
environment:
  ...

  replicas:
    n_workers: 3
```

You can have more control over the created tasks by defining the resources and scheduling of each task
the same way we defined the resources for the master.

Here's an example where we define resources for the master, workers and parameter server.


```yaml
...
framework: horovod
...
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      requests: 1
      limits: 1

  replicas:
    n_workers: 7

    default_worker:
      resources:
        cpu:
          requests: 1
          limits: 2
        memory:
          requests: 256
          limits: 1024
        gpu:
          requests: 1
          limits: 1

    worker:
      - index: 2
        resources:
          cpu:
            requests: 1
            limits: 2
          memory:
            requests: 256
            limits: 1024
          gpu:
            requests: 1
            limits: 1
```

This configuration defines a cluster of 1 master and 7 workers.

The master's resources is defined in the resources section, i.e.

```yaml
resources:
  cpu:
    requests: 1
    limits: 2
  memory:
    requests: 256
    limits: 1024
  gpu:
    requests: 1
    limits: 1
```

The third worker (worker with index == 2) has a specific resources definition:

```yaml
worker_resources:
  - index: 2
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      requests: 1
      limits: 1
```
And all the other workers have the same default worker resources definition, i.e.

```yaml
default_worker:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      requests: 1
      limits: 1
```
