---
title: "Resources Scheduling"
sub_link: "scheduling-strategies/resources-scheduling"
meta_title: "Resources Scheduling in Polyaxon - Scheduling strategies"
meta_description: "Polyaxon schedules workload on Kubernetes, which means you can enable GPU, TPU, or any other resource supported in your cluster for running your operations."
tags:
  - configuration
  - polyaxon
  - kubernetes
  - environment
  - scheduling
  - orchestration
  - nodes
sidebar: "core"
---

Polyaxon schedules workload on Kubernetes, which means you can enable GPU, TPU, or any other resource supported in your cluster for running your operations.

## Prerequisites

If you have not seen this article about [node scheduling](/docs/core/scheduling-strategies/node-scheduling/),
we suggest that you check it out for more details about the options provided
to select which nodes should be used for running your operations.

## Using GPUs

To enable GPUs for your operations, you just need to set the GPU limits/requests on the container resources section, similar to Kubernetes.

```yaml
run:
  kind: job
  container:
    ...
    resources:
      limits:
        nvidia.com/gpu: "2"
...
```

In Python

```python
from polyaxon import k8s

container = k8s.V1Container(
    name="job",
    image="busybox:1.28",
    resources=k8s.V1ResourceRequirements(requests={"nvidia.com/gpu": "2"}),
    command=['sh', '...']
)
```

If the cluster has multiple node pools with different GPU types,
you can specify the GPU type by using a node selector in the [environment section](/docs/core/specification/environment/), e.g. GKE:

```yaml
environment:
  nodeSelector:
    cloud.google.com/gke-accelerator: nvidia-tesla-p4
...
run:
  kind: job
  container:
    ...
    resources:
      limits:
        nvidia.com/gpu: "2"
...
```

In Python

```python
from polyaxon.schemas import V1Environment
from polyaxon import k8s

environment = V1Environment(node_selector={"cloud.google.com/gke-accelerator": "nvidia-tesla-p4"})
container = k8s.V1Container(
    name="job",
    image="busybox:1.28",
    resources=k8s.V1ResourceRequirements(requests={"nvidia.com/gpu": "2"}),
    command=['sh', '...']
)
```

> **Note**: You might need to install [NVIDIA Device Plugin](https://github.com/NVIDIA/k8s-device-plugin).

## Using TPUs

To use [TPUs](https://cloud.google.com/tpu/docs/kubernetes-engine-setup) for your Polyaxon workload on GKE,
you just need to set the TPU limits/requests on the container resources section, similar to Kubernetes,
additionally you need to set the required annotations on the [environment section](/docs/core/specification/environment/).

```yaml
environment:
  annotations:
    tf-version.cloud-tpus.google.com: "1.12"
...
container:
  ...
  resources:
    limits:
      cloud-tpus.google.com/v2: "8"
...
```

In Python

```python
from polyaxon.schemas import V1Environment
from polyaxon import k8s

environment = V1Environment(annotations={"tf-version.cloud-tpus.google.com": "1.12"})
container = k8s.V1Container(
    name="job",
    image="busybox:1.28",
    resources=k8s.V1ResourceRequirements(limits={"cloud-tpus.google.com/v2": "8"}),
    command=['sh', '...']
)
```

## Using other resources

If your cluster has special resources schedulable with Kubernetes, you can use them with Polyaxon,
for instance [AMD GPU](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/#deploying-amd-gpu-device-plugin).

## Sharing GPUs

Aliyun provides a plugin for GPU sharing. You need to deploy the plugin and use the `aliyun.com/gpu-mem` instead of the default `nvidia.com/gpu`.

For more details please check this [user guide](https://github.com/AliyunContainerService/gpushare-scheduler-extender/blob/master/docs/userguide.md).
