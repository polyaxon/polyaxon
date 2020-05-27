---
title: "Node Scheduling"
sub_link: "scheduling-strategies/node-scheduling"
meta_title: "Node Scheduling in Polyaxon - Scheduling strategies"
meta_description: "Polyaxon provides a list of options to select which nodes should be used for a specific operations."
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

Polyaxon provides a list of options to select which nodes should be used for  the operations it runs.

Every component in Polyaxon can set an [environment section](/docs/core/specification/environment/) 
which exposes many pod level options. 

Component's environment section can be [patched](/docs/core/specification/operation/#run_patch) 
by the operation to override the default environment section per execution.

The environment section can be used as well to configure a particular job of a distributed experiment on a specific node,
every replica of a distributed job comes with an environment section.

## Node Name

The simplest form of node selection constraint, but due to its limitations it is typically not used.

```yaml
environment:
  nodeName:
```

## Node Selector

Node selector is the simplest recommended form of node selection constraint.

```yaml
environment:
  nodeSelector:
```

For example, if you have some GPU nodes, you might want to only use them for training your experiments.
In this case you should label your nodes:

```bash
$ kubectl label nodes <node-name> <label-key>=<label-value>
```

And use that label for running experiments.

Example:

```bash
kubectl label nodes worker_1 worker_2 polyaxon.com=experiments
```

And then in your polyaxonfile

```yaml
environment:
  nodeSelector:
    polyaxon.com: experiments
```

This will force Polyaxon to schedule this particular experiment on the specific node(s).

## Tolerations

Tolerations are applied to pods, and allow (but do not require) the pods to schedule onto nodes with matching taints.

Similar to node selector, it's very easy to provide a tolerations in the polyaxonfile:


```yaml

environment:
  tolerations:
    ...
```

## Affinity

The affinity/anti-affinity feature, greatly expands the types of constraints you can express.

```yaml
environment:
  affinity:
    podAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            ...
```
