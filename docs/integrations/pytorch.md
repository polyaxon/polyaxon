---
title: "Pytorch"
meta_title: "Pytorch"
meta_description: "Polyaxon allows to schedule Pytorch experiments and Pytorch distributed experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "PyTorch is an open-source machine learning library for Python, based on Torch, used for applications such as natural language processing. It is primarily developed by Facebook's artificial-intelligence research group, and Uber's Pyro software for probabilistic programming is built on it."
image: "../../content/images/integrations/pytorch.png"
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
status: published
---

Polyaxon allows to schedule Pytorch experiments and Pytorch distributed experiments, and supports tracking metrics, outputs, and models. 
The platform also offers two backends for running Pytorch distributed experiments: native and Kubeflow.

## Overview

By default polyaxon creates a master job, so you only need to add replicas for the workers.

To enable distributed runs, you need to set the `framework` field to `pytroch` and update the `environment` section.

The environment section allows to customize the resources of the master job, as well as defining the topology/replicas of the experiment with a specific definition for each framework.

To customize the master resources, you just need to define the resources in the environment section, e.g.

```yaml
...
framework: pytorch
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

[Distributed Pytorch](http://pytorch.org/tutorials/intermediate/dist_tuto.html) defines a master task (worker with rank 0) and a set of worker tasks.

To define a Pytorch cluster in Polyaxon with a master, 3 workers,
add a replicas subsection to the environment section of your polyaxonfile:


```yaml
...
framework: pytorch
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
framework: pytorch
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

## Distributed experiment backend

By default Polyaxon uses a native behaviour for starting distributed experiments.
 
Polyaxon also supports running distributed experiment on [Kubeflow](/integrations/kubeflow/).

In order to use `kubeflow` as a backend instead of the `native` behaviour, you only need to update your polyaxonfile with `backend` field:

```yaml
version: 1
kind: experiment
backend: kubeflow
framework: pytorch
...
```
