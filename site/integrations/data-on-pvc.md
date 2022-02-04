---
title: "Data on Persistent Volume Claim"
meta_title: "PVC(Persistent Volume Claim)"
meta_description: "Using data on a PVC(Persistent Volume Claim) in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple PVCs to access data directly on your machine learning experiments and jobs."
custom_excerpt: "The PersistentVolume subsystem provides an API for users and administrators that abstracts details of how storage is provided from how it is consumed."
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

You can use one or multiple volumes to access data directly on your machine learning experiments and jobs

## Define or create a PVC

You need to define or create a PVC in the same namespace as Polyaxon CE or Polyaxon Agent.

Under the same namespace where you are deploying Polyaxon, e.g. `polyaxon`, create a PVC using kubectl

```bash
kubectl create -f data-pvc.yaml -n polyaxon
```

> **Tip**: Please visit the Kubernetes documentation to learn about [persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

## Now you can use this PVC to mount data to your experiments and jobs in Polyaxon

```yaml
connections:
- name: dataset1
  kind: volume_claim
  schema:
    mountPath: /plx-data
    volumeClaim: polyaxon-pvc-data
```

To mount the data with the read-only option:


```yaml
connections:
- name: dataset1
  kind: volume_claim
  schema:
    mountPath: /plx-data
    volumeClaim: polyaxon-pvc-data
    readOnly: true
```

If you want ot access multiple datasets:

```yaml
connections:
- name: dataset1
  kind: volume_claim
  schema:
    mountPath: /plx-dataset1
    volumeClaim: polyaxon-pvc-data1
    readOnly: true
- name: dataset2
  kind: volume_claim
  schema:
    mountPath: /plx-dataset2
    volumeClaim: polyaxon-pvc-data2
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
