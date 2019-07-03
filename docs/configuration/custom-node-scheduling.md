---
title: "Customize Node Scheduling"
sub_link: "custom-node-scheduling"
meta_title: "Customize Node Scheduling in Polyaxon - Configuration"
meta_description: "Polyaxon provides a list of options to select which nodes should be used for the core platform, for the dependencies, and for the experiments."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - environment
    - scheduling
    - orchestration
    - nodes
sidebar: "configuration"
---

<blockquote class="warning">This configuration is only available for Polyaxon deployed on Kubernetes clusters.</blockquote>

Polyaxon provides a list of options to select which nodes should be used for the core platform, for the dependencies, and for the runs.


## Node Selectors

### Core and dependencies

Polyaxon comes with a couple of node selectors options to assign pods to nodes for polyaxon's core platform

Additionally every dependency in the helm package, exposes a node selector option.

By providing these values, or some of them,
you can constrain the pods belonging to that category to only run on
particular nodes or to prefer to run on particular nodes.

```yaml
nodeSelector:
  ...
  
postgresql:
  nodeSelector:
    ...

redis:
  nodeSelector:
    ...

rabbitmq-ha:
  nodeSelector:
    ...
    
dockrer-registry:
  nodeSelector:
    ... 
```

### Experiments, jobs, builds, notebooks, tensorboards

For the runs started by users:

  * **experiments**: all user's experiments scheduled by polyaxon
  * **jobs**: all user's generic jobs scheduled by polyaxon
  * **builds**: all build jobs scheduled by polyaxon
  * **notebooks**: all build jobs scheduled by polyaxon
  * **tensorboards**: all tensorboard jobs scheduled by polyaxon
  
You should check the settings page under the scheduling section, to provide default node selectors for each one of these primitives. 

For example, if you have some GPU nodes, you might want to only use them for training your experiments.
In this case you should label your nodes:

```bash
$ kubectl label nodes <node-name> <label-key>=<label-value>
```

And use the same label for `nodeSelectors.experiments`

Example:

```bash
kubectl label nodes worker_1 worker_2 polyaxon.com=experiments
```

And then on the setting page, under `Experiment scheduling`, set the node selector to:

```yaml
polyaxon.com: experiments
```

### Updating node selectors from the Polyaxonfile

In some cases providing a default node selectors for scheduling experiments on some specific nodes is not enough,
for example if the user has labelled 3 nodes with following label:

```bash
$ kubectl label nodes node1 node2 node3 polyaxon: experiments
```

And 1 of these nodes has a specific GPU that the user wishes to use for a particular experiment or for running a Jupyter notebook.

The user can label that node with a label:

```bash
$ kubectl label nodes node3 polyaxon: specific-gpu
```

And use that label to override the default scheduling behavior:

```yaml
version: 1

kind: experiment

environment:
  node_selector:
    polyaxon: specific-gpu

build:
  image: tensorflow/tensorflow:1.4.1-gpu-py3
  build_steps:
    - pip3 install --no-cache-dir -U polyaxon-client

run:
  cmd:  python3 model.py  # Use default params
```

This will force Polyaxon to schedule this particular experiment on that specific node.

This definition can be used in very similar way to schedule a notebook or a tensorboard on that node:

Notebook:

```yaml
version: 1

kind: notebook

environment:
  node_selector:
    polyaxon: specific-gpu

build:
  image: tensorflow/tensorflow:1.4.1-gpu-py3
  build_steps:
    - pip3 install jupyter
```

You can even use that to schedule a particular job of distributed experiment on that node,
for example we can imagine that if the user runs a distributed experiment with a master, 2 workers, and one ps,
and the user wishes to schedule the worker on that node:

```yaml
version: 1

kind: experiment

framework: tensorflow

environment:
  replicas:
    n_workers: 2
    n_ps: 1

  worker:
    - index: 1
      node_selector:
        polyaxon: specific-gpu

build:
  image: tensorflow/tensorflow:1.4.1
  build_steps:
    - pip install --no-cache-dir -U polyaxon-client

run:
  cmd:  python run.py --train-steps=400 --sync

```

This will schedule the master, the ps, and the first worker on any node experiment node,
and will force the second worker to be scheduled on the node with the label `polyaxon=specific-gpu`

## Tolerations

If one or more taints are applied to a node,
and you want to make sure some pods should not deploy on it,
Polyaxon provides tolerations option for the core platform, as well as for all dependencies, e.i. database, broker, expose their own tolerations option.

### Core and dependencies

```yaml
tolerations:
  ...
  
postgresql:
  tolerations:
    ...

redis:
  tolerations:
    ...

rabbitmq-ha:
  tolerations:
    ...
    
dockrer-registry:
  tolerations:
    ... 
```

### Experiments, jobs, builds, notebooks, tensorboards

For the runs started by users:

  * **experiments**: all user's experiments scheduled by polyaxon
  * **jobs**: all user's generic jobs scheduled by polyaxon
  * **builds**: all build jobs scheduled by polyaxon
  * **notebooks**: all build jobs scheduled by polyaxon
  * **tensorboards**: all tensorboard jobs scheduled by polyaxon
  
You should check the settings page under the scheduling section, to provide default tolerations for each one of these primitives. 

### Updating tolerations from the Polyaxonfile

Additionally every Polyaxon users can override the default tolerations by using the Polyaxonfile, e.g.:


```yaml
version: 1

kind: notebook

environment:
  tolerations:
    ...

build:
  image: tensorflow/tensorflow:1.4.1-gpu-py3
  build_steps:
    - pip3 install jupyter
```

## Affinity

### Core and dependencies

It allows you to constrain which nodes your pod is eligible to schedule on, based on the node's labels.
Polyaxon has a default `Affinity` values for it's core components to ensure that they deploy on the same node.

Polyaxon's default affinity:

```yaml
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
              - "polyaxon-core"
          topologyKey: "kubernetes.io/hostname"
```

You can update your config deployment file to set affinity for each dependency:


```yaml
affinity:
  ...
  
postgresql:
  affinity:
    ...

redis:
  affinity:
    ...

rabbitmq-ha:
  affinity:
    ...
    
dockrer-registry:
  affinity:
    ... 
```

### Experiments, jobs, builds, notebooks, tensorboards

For the runs started by users:

  * **experiments**: all user's experiments scheduled by polyaxon
  * **jobs**: all user's generic jobs scheduled by polyaxon
  * **builds**: all build jobs scheduled by polyaxon
  * **notebooks**: all build jobs scheduled by polyaxon
  * **tensorboards**: all tensorboard jobs scheduled by polyaxon
  
You should check the settings page under the scheduling section, to provide default affinity for each one of these primitives. 

### Updating affinity from the Polyaxonfile

Additionally every Polyaxon users can override the default tolerations by using the Polyaxonfile, e.g.:


```yaml
version: 1

kind: tensorbaord

environment:
  affinity:
    ...

build:
  image: tensorflow/tensorflow:1.4.1-py3
```
