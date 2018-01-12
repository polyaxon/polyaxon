Polyaxon provides a list of options to select which nodes
should be used for the core platform, for the dependencies, and for the experiments.


## Node Selectors

Polyaxon comes with 3 node selectors to assign pods to nodes

  * core: the core polyaxon platform
  * dependencies: all polyaxon dependencies, e.i. data base, broker, ...
  * experiments: all user's experiments scheduled by polyaxon

By providing these values, or some of them,
you can constrain the pods belonging to that category to only run on
particular nodes or to prefer to run on particular nodes.

For example, if you have some GPU nodes, you might want to only use them for training your experiments.
In this case you should label your nodes:

```bash
$ kubectl label nodes <node-name> <label-key>=<label-value>
```

And use the same label for `nodeSelectors.experiments`

## Tolerations

If you have some nodes with `Taints` and you you want to use it, Polyaxon provides three tolerations:

  * core: the core polyaxon platform
  * dependencies: all polyaxon dependencies, e.i. data base, broker, ...

## Affinity

It allows you to constrain which nodes your pod is eligible to schedule on, based on labels on the node,
Polyaxon has a default `Affinity` values for both dependencies and core, to ensure they deploy on same node.
Possible values:

  * core: the core polyaxon platform
  * dependencies: all polyaxon dependencies, e.i. data base, broker, ...
