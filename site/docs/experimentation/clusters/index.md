---
title: "Clusters"
sub_link: "clusters"
is_index: true
meta_title: "Clusters in Polyaxon - Experimentation"
meta_description: "Polyaxon supports running Ray and Dask clusters for training or data processing via RayCluster, DaskCluster."
tags:
  - concepts
  - polyaxon
  - experimentation
  - experiments
  - architecture
sidebar: "experimentation"
---

Polyaxon supports running Ray and Dask clusters for distributed computing workloads via Kubernetes operators.

By default, Polyaxon does not deploy the operators required for running clusters to keep the deployment process lightweight.
In order to use a cluster operator, you need to make sure that your namespace/cluster has the operator deployed
or you should deploy the operator(s) before starting an execution.

> When you start a cluster, Polyaxon will stream and archive logs from all replicas.

## Cluster operators

In order to run RayCluster/DaskCluster you will need to deploy their operators before scheduling a cluster from Polyaxon.

## Ray

In order to run Ray clusters you will need to deploy the [KubeRay](https://docs.ray.io/en/latest/cluster/kubernetes/index.html) operator before scheduling a cluster from Polyaxon.

```yaml
version: 1.1
kind: component
name: ray-cluster
run:
  kind: raycluster
  rayVersion: '2.9.0'
  head:
    container:
      image: rayproject/ray:2.9.0
  workers:
    small:
      replicas: 2
      minReplicas: 1
      maxReplicas: 3
      container:
        image: rayproject/ray:2.9.0
```

The same example in Python:

```python
from polyaxon.schemas import V1Component, V1RayCluster, V1RayReplica
from polyaxon import k8s

ray_cluster = V1RayCluster(
    ray_version="2.9.0",
    head=V1RayReplica(
        container=k8s.V1Container(image="rayproject/ray:2.9.0"),
    ),
    workers={
        "small": V1RayReplica(
            replicas=2,
            min_replicas=1,
            max_replicas=3,
            container=k8s.V1Container(image="rayproject/ray:2.9.0"),
        ),
    },
)

component = V1Component(name="ray-cluster", run=ray_cluster)
```

### RayCluster with Autoscaling

```yaml
version: 1.1
kind: component
name: ray-cluster-autoscaling
run:
  kind: raycluster
  rayVersion: '2.9.0'
  enableInTreeAutoscaling: true
  head:
    rayStartParams:
      dashboard-host: '0.0.0.0'
    container:
      image: rayproject/ray:2.9.0
      resources:
        limits:
          cpu: "1"
          memory: 2Gi
        requests:
          cpu: 500m
          memory: 1Gi
  workers:
    cpu-workers:
      replicas: 2
      minReplicas: 1
      maxReplicas: 5
      container:
        image: rayproject/ray:2.9.0
        resources:
          limits:
            cpu: "1"
            memory: 2Gi
          requests:
            cpu: 500m
            memory: 1Gi
```

### RayCluster with Runtime Environment

```yaml
version: 1.1
kind: component
name: ray-cluster-runtime
run:
  kind: raycluster
  rayVersion: '2.9.0'
  entrypoint: python train.py
  runtimeEnv:
    pip: ["requests==2.26.0", "pandas==2.0.0"]
    env_vars:
      MY_ENV_VAR: "value"
  head:
    container:
      image: rayproject/ray:2.9.0
  workers:
    default:
      replicas: 2
      container:
        image: rayproject/ray:2.9.0
```

### Specification

Please check the [RayCluster](/docs/experimentation/clusters/ray-clusters/) guide to learn about all details for running Ray clusters in Polyaxon.

## Dask

In order to run Dask clusters you will need to deploy the [dask-kubernetes](https://kubernetes.dask.org/) operator before scheduling a cluster from Polyaxon.

```yaml
version: 1.1
kind: component
name: dask-cluster
run:
  kind: daskcluster
  worker:
    replicas: 2
    container:
      image: ghcr.io/dask/dask:latest
  scheduler:
    container:
      image: ghcr.io/dask/dask:latest
```

The same example in Python:

```python
from polyaxon.schemas import V1Component, V1DaskCluster, V1DaskReplica
from polyaxon import k8s

dask_cluster = V1DaskCluster(
    worker=V1DaskReplica(
        replicas=2,
        container=k8s.V1Container(image="ghcr.io/dask/dask:latest"),
    ),
    scheduler=V1DaskReplica(
        container=k8s.V1Container(image="ghcr.io/dask/dask:latest"),
    ),
)

component = V1Component(name="dask-cluster", run=dask_cluster)
```

### DaskCluster with Autoscaling

```yaml
version: 1.1
kind: component
name: dask-cluster-autoscaling
run:
  kind: daskcluster
  minReplicas: 1
  maxReplicas: 10
  worker:
    replicas: 2
    container:
      image: ghcr.io/dask/dask:latest
      resources:
        requests:
          memory: 2Gi
          cpu: 1
        limits:
          memory: 4Gi
          cpu: 2
  scheduler:
    container:
      image: ghcr.io/dask/dask:latest
      resources:
        requests:
          memory: 1Gi
          cpu: 500m
```

### Specification

Please check the [DaskCluster](/docs/experimentation/clusters/dask-clusters/) guide to learn about all details for running Dask clusters in Polyaxon.
