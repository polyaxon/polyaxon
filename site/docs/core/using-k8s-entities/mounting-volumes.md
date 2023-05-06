---
title: "How to mount volumes manually"
sub_link: "using-k8s-entities/mounting-volumes"
meta_title: "A guide on mounting volumes manually - Core Concepts"
meta_description: "While we generally recommend that users should leverage the connection interface to configure and abstract requesting and mounting volumes, it's possible to mount volumes manually."
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
to configure and abstract requesting and mounting volumes for the [artifacts store](/integrations/artifacts/) or for [datasets](/integrations/data-stores/).
It is sometimes much easier to mount a volume manually if the volume will be used temporarily or for testing purposes.

## Usage

Polyaxon exposes the `volumes` section on all runtime kinds and the full container specification to mount the volumes defined in containers.
In this section, we will demonstrate how to mount a volume manually in a job, but the same steps can be followed to mount volumes in services or distributed jobs.

```yaml
kind: component
...
run:
  kind: job

  volumes:
  - name: volume1
    persistentVolumeClaim:
      claimName: pvc1
  - name: volume2
    hostPath:
      path: /path/to/use
  container:
    volumeMounts:
    - name: volume1
      mountPath: /mnt1/vol1/path
    - name: volume2
      mountPath: /mnt2/vol2/path
```

## Moving Volumes to connections

If you find yourself defining the same volumes in all operations, or if you have non-Kubernetes experts using Polyaxon,
we suggest that you define those volumes as [connections](/integrations/data-on-pvc/), by doing so,
users of the cluster will just request those volumes using a single line:

```yaml
kind: component
...
run:
  kind: job
  connections: [volume1, volume2]
```

Polyaxon will take care of the mechanics of converting those connections to volumes and mounts.
