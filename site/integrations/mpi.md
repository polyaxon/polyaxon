---
title: "MPI"
meta_title: "mpi"
meta_description: "Polyaxon allows to schedule distributed MPI experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "The MPI Operator makes it easy to run allreduce-style distributed training."
image: "../../content/images/integrations/mpi.png"
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

Polyaxon allows to schedule distributed MPI experiments, and supports tracking metrics, outputs, and models.

## Overview

In order to use the `mpi` backend, users need to install the [MPIJob](/integrations/kubeflow/#deployingdeleting-mpijob).

To enable distributed runs, you need to set the `backend` field to `mpi` and update the `environment` section.

You can annotate your experiments with any framework you are using, it's optional.

The environment section allows to customize the resources as well as defining the topology/replicas of the experiment.

## Define the distributed topology

To define a cluster in Polyaxon with 2 workers,
add a replicas subsection to the environment section of your polyaxonfile:


```yaml
...
framework: mpi
...
environment:
  replicas:
    n_workers: 2
    default_worker:
      resources:
        gpu:
          requests: 1
          limits: 1
```

Since the MPIOperator does not allow to expose specific resources for the different workers, you can only use the default worker subsection to define the default resources for all workers.
