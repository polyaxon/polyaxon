---
title: "Tensorflow"
meta_title: "Tensorflow"
meta_description: "Polyaxon allows to schedule Tensorflow experiments and Tensorflow distributed experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "TensorFlow is an open source software library for high performance numerical computation. Its flexible architecture allows easy deployment of computation across a variety of platforms (CPUs, GPUs, TPUs)."
image: "../../content/images/integrations/tensorflow.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - tracking
  - scheduling
  - distributed-training
featured: false
visibility: public
status: published
---

## Overview

By default polyaxon creates a master job, so you only need to provide the workers and/or parameter servers.

To enable distributed runs, you need to update the environment section.

The environment section allows to customize the resources of the master job, as well as defining the topology of the experiment with a specific definition for each framework.

To customize the master resources, you just need to define the resources in the environment section, e.g.

```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      request: 1
      limits: 1
```

## Define the distributed topology

To [distribute Tensorflow](https://www.tensorflow.org/deploy/distributed) experiment,
the user needs to define a cluster, which is a set of tasks that participate in the distributed execution.

Tensorflow defines 3 different types of tasks: master, worker, and parameter server.

To define a cluster in Polyaxon with a master, 3 workers, and 1 parameter server,
add a tensorflow subsection to the environment section of your polyaxonfile:

```yaml
...

environment:
  ...

  tensorflow:
    n_workers: 3
    n_ps: 1
```

You can have more control over the created tasks by defining the resources and scheduling of each task
the same way we defined the resources for the master.

Here's an example where we define resources for the master, workers and parameter server.


```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      request: 1
      limits: 1

  tensorflow:
    n_workers: 7
    n_ps: 3

    default_worker:
      resources:
        cpu:
          requests: 1
          limits: 2
        memory:
          requests: 256
          limits: 1024
        gpu:
          request: 1
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

    default_ps:
      resources:
        cpu:
          requests: 1
          limits: 1
        memory:
          requests: 256
          limits: 256

    ps:
      - index: 0
        resources:
          cpu:
            requests: 1
            limits: 1
          memory:
            requests: 512
            limits: 512
```

This configuration defines a cluster of 1 master, 7 workers, and 3 parameter servers.

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
    request: 1
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
      request: 1
      limits: 1
```

Same logic applies to the parameter servers with the `default_ps.resources` and `ps_resources`.
