---
title: "How to mount secrets manually"
sub_link: "using-k8s-entities/mounting-secrets"
meta_title: "A guide on mounting secrets manually - Core Concepts"
meta_description: "While we generally recommend that users should leverage the connection interface to configure and abstract requesting and mounting secrets, it's possible to mount secrets manually."
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
to configure and abstract requesting and mounting secrets.
It is sometimes much easier to mount a secret manually if the secret will be used temporarily or for testing purposes.

Polyaxon supports similar secrets syntax and mechanisms as Kubernetes Pod specs, 
which allows access to secrets as environment variables or volume mounts. For more information, 
please check [the Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/secret/).

## Usage as environment variables

In this section, we will demonstrate how to mount a secret manually as environment variables in a job, but the same steps can be followed to mount secrets in services or distributed jobs.

```yaml
kind: component
...
run:
  kind: job
  container:
    command: ..
    envFrom:
    - secretRef:
      name: my-secret1
    - secretRef:
      name: my-secret2
    env:
    - name: secret-name
      valueFrom:
        secretKeyRef:
          name: my-secret3
          key: secret-key
```

## Usage as a volume

In this section, we will demonstrate how to mount secrets manually as volumes in a job, but the same steps can be followed to mount secrets in services or distributed jobs.

```yaml
kind: component
...
run:
  kind: job
  volumes:
  - name: secret-vol-name
    secret:
      secretName: my-secret
  container:
    command: ..
    volumeMounts:
    - name: secret-vol-name
      mountPath: "/etc/secret/path"
      readOnly: true
```

## Moving secrets to connections

If you find yourself defining the same secrets in all operations, or if you have non-Kubernetes experts using Polyaxon, 
we suggest that you define those secrets as custom connections, by doing so, users of the cluster will just request those secrets using a single line:

```yaml
kind: component
...
run:
  kind: job
  connections: [secret1, secret2]
```

Polyaxon will take care of the mechanics of converting those connections to environment variables or volumes and mounts.
