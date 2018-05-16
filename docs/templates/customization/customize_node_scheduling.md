Polyaxon provides a list of options to select which nodes
should be used for the core platform, for the dependencies, and for the experiments.


## Node Selectors

Polyaxon comes with 2 node selectors to assign pods to nodes

  * `core`: the core polyaxon platform
  * `experiments`: all user's experiments scheduled by polyaxon

Additionally every dependency in our helm package, exposes a node selector option.

By providing these values, or some of them,
you can constrain the pods belonging to that category to only run on
particular nodes or to prefer to run on particular nodes.

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

```yaml
nodeSelectors:
  experiments:
    polyaxon.com: experiments
```

### Experiments and Jobs node selectors

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
---
version: 1

kind: experiment

environment:
  node_selectors:
    polyaxon: specific-gpu

run:
  image: tensorflow/tensorflow:1.4.1-gpu-py3
  build_steps:
    - pip3 install --no-cache-dir -U polyaxon-helper
  cmd:  python3 model.py  # Use default params
```

This will force Polyaxon to schedule this particular experiment on that specific node.

This definition can be used in very similar way to schedule a notebook or a tensorboard on that node:

Notebook:

```yaml
---
version: 1

kind: plugin

environment:
  node_selectors:
    polyaxon: specific-gpu

run:
  image: tensorflow/tensorflow:1.4.1-gpu-py3
  build_steps:
    - pip3 install jupyter
```

You can even use that to schedule a particular job of distributed experiment on that node,
for example we can imagine that if the user runs a distributed experiment with a master, 2 workers, and one ps,
and the user wishes to schedule the worker on that node:

```yaml
---
version: 1

kind: experiment

environment:
  tensorflow:
    n_workers: 2
    n_ps: 1

  worker_node_selectors:
    - index: 1
      polyaxon: specific-gpu

run:
  image: tensorflow/tensorflow:1.4.1
  build_steps:
    - pip install --no-cache-dir -U polyaxon-helper
  cmd:  python run.py --train-steps=400 --sync

```

This will schedule the master, the ps, and the first worker on any node experiment node,
and will force the second worker to be scheduled on the node with the label `polyaxon=specific-gpu`

## Tolerations

If one or more taints are applied to a node,
and you want to make sure some pods should not deploy on it,
Polyaxon provides tolerations option for the core platform as well as for all dependencies,
e.i. database, broker, expose their own tolerations option.

Example for core platform:

```yaml
tolerations:
  core:
    ...
```

Example for Rabbitmq:

```yaml
rabbitmq:
  tolerations:
    ...
```

## Affinity

It allows you to constrain which nodes your pod is eligible to schedule on, based on the node's labels.
Polyaxon has a default `Affinity` values for both dependencies and core to ensure that they deploy on the same node.
