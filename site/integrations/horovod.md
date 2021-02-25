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
  - operators
  - distributed-training
  - scheduling
featured: false
popularity: 1
visibility: public
---

Polyaxon allows to schedule distributed Horovod experiments, and supports tracking metrics, outputs, and models.

## Experiments on a single node

To run experiments on single node with Horovod, you don't need to deploy the MPIOperator, you just need to provide the correct command and args to enable usage of Horovod.

```yaml
version: 1.1
kind: component
inputs:
  - name: gpus
    isOptional: true
    type: int
    value: 2
run:
  kind: job
  container:
      image: IMAGE_TO_USE
      resources:
          limits:
            nvidia.com/gpu: "{{ gpus }}"
      command: ["horovodrun", "-np", "{{ gpus }}", "-H", "localhost:{{ gpus }}", "python", "-u", "mnist.py"]
```

## Distributed experiments with the MPIJob Operator

Polyaxon provides support for Horovod via the [MPIJob Operator](/integrations/mpijob/). So you will need to deploy the operator first and then provide a valid MPIJob manifest.

## Define the distributed topology

Please check the guide [Running Horovod](https://github.com/horovod/horovod#running-horovod) for more details on how to set a Horovod experiment with MPI.

Example manifest:

```yaml
version: 1.1
kind: component
run:
  kind: mpijob
  slotsPerWorker: 1
  launcher:
    replicas: 1
    container:
      image: docker.io/kubeflow/mpi-horovod-mnist
      command:
        - mpirun
      args:
        - -np
        - "2"
        - --allow-run-as-root
        - -bind-to
        - none
        - -map-by
        - slot
        - -x
        - LD_LIBRARY_PATH
        - -x
        - PATH
        - -mca
        - pml
        - ob1
        - -mca
        - btl
        - ^openib
        - python
        - /examples/tensorflow_mnist.py
      resources:
        limits:
          cpu: 1
          memory: 2Gi
  worker:
    replicas: 2
    container:
      image: docker.io/kubeflow/mpi-horovod-mnist
      resources:
        limits:
          cpu: 2
          memory: 4Gi
```
