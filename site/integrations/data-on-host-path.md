---
title: "Data on Node Host Path"
meta_title: "Node Host Path(host node's filesystem)"
meta_description: "Using Node Host Path in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple host node's filesystem to access data directly on your machine learning experiments and jobs."
custom_excerpt: "A hostPath volume mounts a file or directory from the host node's filesystem into your Pod. This is not something that most Pods will need, but it offers a powerful escape hatch for some applications."
image: "../../content/images/integrations/pvc.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - data-stores
  - storage
featured: false
popularity: 0
visibility: public
status: published
---

You can use one or multiple node host paths (host node's filesystem) to access data directly on your machine learning experiments and jobs

> **Tip**: Please visit the Kubernetes documentation to learn about [host paths](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath).


## Use the host path as a connection

```yaml
connections:
- name: node-dataset
  kind: host_path
  schema:
    mountPath: "/path/dataset"
    hostPath: "/path/to/dataset"
```

To mount the data with the read-only option:


```yaml
connections:
- name: node-dataset
  kind: host_path
  schema:
    mountPath: "/path/dataset"
    hostPath: "/path/to/dataset"
    readOnly: true
```

If you want ot access multiple datasets:

```yaml
connections:
- name: dataset1
  kind: host_path
  schema:
    mountPath: /plx-dataset1
    hostPath: "/path/to/dataset1"
    readOnly: true
- name: dataset2
  kind: host_path
  schema:
    mountPath: /plx-dataset2
    hostPath: "/path/to/dataset2"
    readOnly: true
```

## Update/Install Polyaxon CE or Polyaxon Agent deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to data on the PVC.

## Access to the dataset in your experiments/jobs

To expose the connection secret to one of the containers in your jobs or services:

```yaml
run:
  kind: job
  connections: [dataset1]
```

Or

```yaml
run:
  kind: job
  connections: [dataset1, s3-dataset1]
```

## Use the initializer to load the dataset

To use the artifacts initializer to load the dataset

```yaml
run:
  kind: job
  init:
   - artifacts: {dirs: [...], files: [...]}
     connection: "dataset1"
```
