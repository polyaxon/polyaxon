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
      request: 1
      limits: 1
    tpu:
      request: 8
      limits: 8
```

## outputs

Sometime you experiment or your job might depend on previous jobs or experiments,
and you need to use their outputs to either do fine tuning or post processing of those outputs.

Outputs gives you a way to reference outputs from previous experiments and jobs,
by either using their ids or names (if you gave them name).

This will both mount necessary outputs volumes,
and will expose the paths of those outputs in your experiment/job that requested them.

If you referenced different outputs from jobs and experiments, the paths will following
the same order that was provided.

```yaml
environment:
  outputs:
    jobs: [1, 234, 'job_name1', 'another_username/another_project/job_name2']
    experiments: [12, 'experiment_name', 'my_other_project/experiment_name2']
```

## persistence

The volumes to mount for data and outputs, this is only needed when Polyaxon was deployed
with multiple data volumes or multiple outputs volumes or both.

```yaml
environment:
  persistence:
    data: ['data_volume_name1', 'data_volume_name2', 'data_volume_name3']
    outputs: 'outputs_volume_name2'
```

## node selectors

The labels to use as node selectors for scheduling the job on a specific node.
You can also set default [node selectors](/reference_polyaxon_helm/#node-and-deployment-manipulation)
during the deployment and use this subsection to override the default values.

```yaml
environment:
  node_selector:
    node_label: node_value
```

## tolerations

The tolerations to use for the scheduling the job.
You can also set default [tolerations](/reference_polyaxon_helm/#node-and-deployment-manipulation)
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
You can also set default [affinity](/reference_polyaxon_helm/#node-and-deployment-manipulation)
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

## configmap_refs

A list of config map references to mount during the scheduling of a job/build/experiment

```yaml
environment:
  configmap_refs: ['configmap1', 'configmap3']
```

## secret_refs

```yaml
environment:
  secret_refs: ['secret1', 'secret2']
```

A list of secret references to mount during the scheduling of a job/build/experiment

## tensorflow

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

  tensorflow:
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
            request: 1
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

      ps_resources:
        - index: 0
          cpu:
            requests: 1
            limits: 1
          memory:
            requests: 256
            limits: 1024
```

## mxnet

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

environment:
  mxnet:
    n_workers: 4
    n_ps: 1

    default_ps:
      node_selector:
        polyaxon: nodes_for_param_servers
```

## pytorch

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

environment:
  pytorch:
    n_workers: 4
```

## horovod

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

environment:
  horovod:
    n_workers: 4
```
