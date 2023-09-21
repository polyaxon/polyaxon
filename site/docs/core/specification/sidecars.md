---
title: "Sidecars Specification"
sub_link: "specification/sidecars"
meta_title: "Sidecar - Polyaxon Specification"
meta_description: "Sidecar section provides a way to run specialized containers as sidecars to the main container."
visibility: public
status: published
tags:
  - specification
  - api
  - polyaxon
  - yaml
  - json
  - python
sidebar: "core"
---

Sidecars section provides a way to run specialized containers as sidecars to the main container.

Polyaxon by default injects its own sidecar container that collects outputs and artifacts,
and users can run any additional sidecar containers.

the sidecar section accepts a list of [Kubernetes Containers](https://kubernetes.io/docs/concepts/containers/).

## Yaml usage

```yaml
version: 1.1
kind: component
run:
  kind: job
  sidecars:
    - name: sidecar1
      image: busybox:1.28
      command: ['sh', '-c', 'echo sidecar1']
      resources:
        requests:
          memory: "128Mi"
          cpu: "500m"
    - name: sidecar2
      image: busybox:1.28
      command: ['sh', '-c', 'echo sidecar2']
  container:
    ...
```

## Python usage

```python
from polyaxon.schemas import V1Component, V1Job
from polyaxon import k8s

component = V1Component(
    run=V1Job(
        sidecars=[
            k8s.V1Container(
                name="sidecar1",
                image="busybox:1.28",
                resources=k8s.V1ResourceRequirements(
                    requests={"memory": "256Mi", "cpu": "500m"}),
                command=['sh', '-c', 'echo sidecar1']
            ),
            k8s.V1Container(
                name="sidecar2",
                image="busybox:1.28",
                command=['sh', '-c', 'echo sidecar2']
            )
        ],
        container=k8s.V1Container(...)
    )
)
```
