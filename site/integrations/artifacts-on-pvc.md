---
title: "Artifacts on Persistent Volume Claim"
meta_title: "PVC(Persistent Volume Claim)"
meta_description: "Using PVC(Persistent Volume Claim) to organize your jobs' outputs and experiments' artifacts. Polyaxon allows users to connect to one or multiple PVCs(Persistent Volume Claim) to store job outputs and experiment artifacts."
custom_excerpt: "The PersistentVolume subsystem provides an API for users and administrators that abstracts details of how storage is provided from how it is consumed."
image: "../../content/images/integrations/pvc.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - artifacts
  - storage
featured: false
popularity: 0
visibility: public
status: published
---

You can use one or multiple PVCs(Persistent Volume Claim) to store logs, job outputs, and experiment artifacts.

## Define or create a PVC

You need to define or create a PVC in the same namespace as Polyaxon CE or Polyaxon Agent.

Under the same namespace where you are deploying Polyaxon, e.g. `polyaxon`, create a PVC using kubectl

```bash
kubectl create -f data-pvc.yaml -n polyaxon
```

> **Tip**: Please visit the Kubernetes documentation to learn about [persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

## Now you can use this PVC as an artifacts store

```yaml
artifactsStore:
  name: artifacts-pvc
  kind: volume_claim
  schema:
    mountPath: /plx-data
    volumeClaim: polyaxon-pvc-data
```

## Update/Install Polyaxon CE or Polyaxon Agent deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to the PVC.
