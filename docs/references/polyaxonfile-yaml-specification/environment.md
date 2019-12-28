---
title: "Environment - Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification/environment"
meta_title: "Environment Section - Polyaxonfile YAML Specification Sections - Polyaxon References"
meta_description: "Environment Section - Polyaxonfile YAML Specification Sections."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

## Overview

The environment section allows to alter the
resources and configuration of the runtime of your experiments.

Based on this section you can define, how many workers/ps you want to run,
the resources, the node selectors, and the configs of each job.

The values of this section are:

## resources

The resources to use for the job. In the case of distributed run, it's the resources to use for the master job.
A resources definition, is optional and made of three optional fields:

 * cpu: {limits: value, requests: value}
 * memory: {limits: value, requests: value}
 * gpu: {limits: value, requests: value}
 * tpu: {limits: value, requests: value} 


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
      requests: 1
      limits: 1
    tpu:
      requests: 8
      limits: 8
```

## node_selector

The labels to use as node selectors for scheduling the job on a specific node.
You can also set default [node selectors](/references/polyaxon-helm-reference/#node-and-deployment-manipulation)
during the deployment and use this subsection to override the default values.

```yaml
environment:
  node_selector:
    node_label: node_value
```

## tolerations

The tolerations to use for the scheduling the job.
You can also set default [tolerations](/references/polyaxon-helm-reference/#node-and-deployment-manipulation)
during the deployment and use this subsection to override the default values.

```yaml
environment:
  tolerations:
    - key: "key"
      operator: "Exists"
      effect: "NoSchedule"
```

## affinity

The affinity to use for the scheduling the job.
You can also set default [affinity](/references/polyaxon-helm-reference/#node-and-deployment-manipulation)
during the deployment and use this subsection to override the default values.

```yaml
environment:
  affinity:
    podAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchExpressions:
              - key: type
                operator: In
                values:
                - "polyaxon-experiments"
            topologyKey: "kubernetes.io/hostname"
```

To enable a distributed run, the user can define one of the following framework:

## annotations

The annotations to inject during the scheduling of the job.

```yaml
environment:
  annotations:
    key1: "value1"
    key2: "value2"
```

## labels

The labels to inject during the scheduling of the job.

```yaml
environment:
  labels:
    key1: "label1"
    key2: "label2"
```

## persistence [deprecated]

This section is deprecated in favor of: `data_refs`, `artifact_refs` and will be remove in future versions.
 
The volumes to mount for data and outputs, this is only needed when Polyaxon was deployed
with multiple data volumes or multiple outputs volumes or both.

```yaml
environment:
  persistence:
    data: ['data_volume_name1', 'data_volume_name2', 'data_volume_name3']
    outputs: 'outputs_volume_name2'
```

## data_refs

The volumes to mount for data and outputs, this is only needed when Polyaxon was deployed
with multiple data volumes.

```yaml
environment:
  data_refs: ['data_volume_name1', 'data_volume_name2', 'data_volume_name3']
```


## config\_map\_refs

> Please note that previously this section used to be `configmaps_refs`

A list of config map references to mount during the scheduling of a job/build/experiment/notebooks/tensorboards

```yaml
environment:
  config_map_refs: ['configmap1', 'configmap3']
```

N.B. the references must be declared by the admin in the catalog to allow access to the resources.

## secret_refs

```yaml
environment:
  secret_refs: ['secret1', 'secret2']
```

A list of secret references to mount during the scheduling of a job/build/experiment/notebooks/tensorboards

N.B. the references must be declared by the admin in the catalog to allow access to the resources.

## service_account

```yaml
environment:
  service_account: 'my-custom-service-account'
```

A custom service account to use during the scheduling of a job/build/experiment/notebooks/tensorboards

## max_restarts

```yaml
environment:
  max_restarts: 4
```

How many times to allow a pod restarts when running job/build/experiment/notebooks/tensorboards in case of an error.

## outputs

Sometime you experiment or your job might depend on previous jobs or experiments,
and you need to use their outputs to either do fine tuning or post processing of those outputs.

Outputs gives you a way to reference outputs from previous experiments and jobs,
by either using their ids or names (if you gave them name).

This will both mount necessary outputs volumes,
and will expose the paths of those outputs in your experiment/job that requested them.

If you referenced different outputs from jobs and experiments, the paths will follow
the same order that was provided.

```yaml
environment:
  outputs:
    jobs: [1, 234, 'job_name1', 'another_username/another_project/job_name2']
    experiments: [12, 'experiment_name', 'my_other_project/experiment_name2']
```

## backend

Defined the backend to be used when running distributed experiments, possible values: `native` (default), `kubeflow`, `mpi`, and `external` when the experiment is tracked outside of Polyaxon.

## framework

Is field to annotate your experiment with the backend used, e.g. `scikit-learn` or `xgboost`.

The framework is required when using a distributed experiment, Polyaxon detects this value and create required replicas and infrastructure to run the distributed experiment for the defined framework.

## framework: tensorflow

### n_workers

The number of workers to use for an experiment.

### n_ps

The number of parameter server to use for an experiment.

### default_worker

Default environment specification to use for all workers.

```yaml
environment:
  default_worker:
    resources:
    node_selector:
    affinity:
    tolerations:
```

### default_ps

Default environment specification to use for all ps.

```yaml
environment:
  default_ps:
    resources:
    node_selector:
    affinity:
    tolerations:
```

### worker

Defines a specific worker(s)' environment section defining, indicated by index:

```yaml
environment:
  worker:
    - index: i
      resources:
      node_selector:
      affinity:
      tolerations:
```

### ps

Defines a specific ps(s)' environment section defining, indicated by index:

```yaml
environment:
  ps:
    - index: i
      resources:
      node_selector:
      affinity:
      tolerations:
```

Example:

```yaml
...
framework: tensorflow
...
environment:

  node_selector:
    polyaxon: experiments

  affinity:
    podAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchExpressions:
              - key: type
                operator: In
                values:
                - "polyaxon-experiments"
            topologyKey: "kubernetes.io/hostname"

  tolerations:
    - key: "key"
      operator: "Exists"
      effect: "NoSchedule"

  resources:
    cpu:
      requests: 2
      limits: 4
    memory:
      requests: 512
      limits: 2048

  replicas:
      n_workers: 4
      n_ps: 1

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
        tolerations:
          - operator: "Exists"

      worker:
        - index: 2
          resources:
            cpu:
              requests: 1
              limits: 2
            memory:
              requests: 256
              limits: 1024
        - index: 3
          node_selector:
            polyaxon: special_node
          tolerations:
            - key: "key"
              operator: "Exists"

      ps:
        - index: 0
          resources:
            cpu:
              requests: 1
              limits: 1
            memory:
              requests: 256
              limits: 1024
```

## framework: mxnet

### n_workers

The number of workers to use for an experiment.

### n_ps

The number of parameter server to use for an experiment.

### default_worker

Default environment specification to use for all workers.

```yaml
environment:
  default_worker:
    resources:
    node_selector:
    affinity:
    tolerations:
```

### default_ps

Default environment specification to use for all ps.

```yaml
environment:
  default_ps:
    resources:
    node_selector:
    affinity:
    tolerations:
```

### worker

Defines a specific worker(s)' environment section defining, indicated by index:

```yaml
environment:
  worker:
    - index: i
      resources:
      node_selector:
      affinity:
      tolerations:
```

### ps

Defines a specific ps(s)' environment section defining, indicated by index:

```yaml
environment:
  ps:
    - index: i
      resources:
      node_selector:
      affinity:
      tolerations:
```

Example:

```yaml
framework: mxnet 
environment:
  replicas:
    n_workers: 4
    n_ps: 1

    default_ps:
      node_selector:
        polyaxon: nodes_for_param_servers
```

## framework: pytorch

### n_workers

The number of workers to use for an experiment.

### default_worker

Default environment specification to use for all workers.

```yaml
environment:
  default_worker:
    resources:
    node_selector:
    affinity:
    tolerations:
```

### worker

Defines a specific worker(s)' environment section defining, indicated by index:

```yaml
environment:
  worker:
    - index: i
      resources:
      node_selector:
      affinity:
      tolerations:
```

Example:

```yaml
framework: pytorch
environment:
  replicas:
    n_workers: 4
```

## framework: horovod

### n_workers

The number of workers to use for an experiment.


### default_worker

Default environment specification to use for all workers.

```yaml
environment:
  default_worker:
    resources:
    node_selector:
    affinity:
    tolerations:
```

### worker

Defines a specific worker(s)' environment section defining, indicated by index:

```yaml
environment:
  worker:
    - index: i
      resources:
      node_selector:
      affinity:
      tolerations:
```

Example:

```yaml
framework: horovod
environment:
  replicas:
    n_workers: 4
```
