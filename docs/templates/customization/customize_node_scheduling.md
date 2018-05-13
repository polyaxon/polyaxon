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
