---
title: "Artifacts on Node Host Path"
meta_title: "Node Host Path(host node's filesystem)"
meta_description: "Using Node Host Path to organize your jobs' outputs and experiments' artifacts. Polyaxon allows users to connect to one or multiple host node's filesystem to store job outputs and experiment artifacts."
custom_excerpt: "A hostPath volume mounts a file or directory from the host node's filesystem into your Pod. This is not something that most Pods will need, but it offers a powerful escape hatch for some applications."
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

You can use one or multiple node host paths (host node's filesystem) to store logs, job outputs, and experiment artifacts.

> **Tip**: Please visit the Kubernetes documentation to learn about [host paths](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath).

## Use the host path as an artifacts store


```yaml
artifactsStore:
  name: node-artifacts-store
  kind: host_path
  schema:
    mountPath: "/artifacts"
    hostPath: "/path/to/artifacts"
```

## Update/Install Polyaxon CE or Polyaxon Agent deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to the PVC.
