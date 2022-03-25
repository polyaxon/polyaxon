---
title: "How to mount configmaps manually"
sub_link: "using-k8s-entities/mounting-configmaps"
meta_title: "A guide on mounting configmaps manually - Core Concepts"
meta_description: "While we generally recommend that users should leverage the connection interface to configure and abstract requesting and mounting configmaps, it's possible to mount configmaps manually."
visibility: public
status: published
tags:
  - specification
  - api
  - polyaxon
  - yaml
  - json
  - python
  - concepts
sidebar: "core"
---

## Overview

While we generally recommend that users should leverage the [connection interface](/docs/setup/connections/)
to configure and abstract requesting and mounting configmaps.
It is sometimes much easier to mount a configmap manually if the configmap will be used temporarily or for testing purposes.

Polyaxon supports similar secrets syntax and mechanisms as Kubernetes Pod specs, 
which allows access to configmaps as environment variables or volume mounts. For more information, 
please check [the Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/configmap/).

## Usage as environment variables

In this section, we will demonstrate how to mount configmaps manually as environment variables in a job, but the same steps can be followed to mount configmaps in services or distributed jobs.

```yaml
kind: component
...
run:
  kind: job
  container:
    command: ..
    envFrom:
    - configMapRef:
      name: my-configmap1
    - configMapRef:
      name: my-configmap2
    env:
    - name: secret-name
      valueFrom:
        configMapKeyRef:
          name: my-configmap3
          key: secret-key
```

## Usage as a volume

In this section, we will demonstrate how to mount a configmaps manually as volumes in a job, but the same steps can be followed to mount configmaps in services or distributed jobs.

```yaml
kind: component
...
run:
  kind: job
  volumes:
  - name: config-vol-name
    configMap:
      name: config-name
      items:
      ...
  container:
    command: ..
    volumeMounts:
    - name: config-vol-name
      mountPath: "/config/path"
      readOnly: true
```

## Moving secrets to connections

If you find yourself defining the same configmaps in all operations, or if you have non-Kubernetes experts using Polyaxon, 
we suggest that you define those configmaps as custom connections, by doing so, users of the cluster will just request those configmaps using a single line:

```yaml
kind: component
...
run:
  kind: job
  connections: [config1, config2]
```

Polyaxon will take care of the mechanics of converting those connections to environment variables or volumes and mounts.
