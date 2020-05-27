---
title: "Outputs on NFS Provisioner"
meta_title: "NFS Provisioner"
meta_description: "Using outputs on an NFS server provisioner in your Polyaxon experiments and jobs. This integration simplifies the creation of ReadWriteMany and ReadOnlyMany volumes."
custom_excerpt: "Polyaxon in-cluster NFS provisioner to simplify the creation of ReadWriteMany and ReadOnlyMany volumes."
image: "../../content/images/integrations/nfs-provisioner.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - artifacts-store
  - storage
featured: false
visibility: public
status: published
---

Polyaxon in-cluster NFS provisioner to simplify the creation of ReadWriteMany and ReadOnlyMany volumes.


## Overview

This guide shows how to use the NFS provisioner to mount outputs to your jobs and experiments. 

[polyaxon-nfs-provisioner](https://github.com/polyaxon/polyaxon-nfs-provisioner) provides a stable Helm chart, maintained and supported by Polyaxon, to easily deploy and spin NFS-volumes to use with Polyaxon. 

## Install

To install the nfs-provisioner, make sure you have helm installed, please see this [guide](/docs/guides/setup-helm/).


## Namespace

If you are using this chart with Polyaxon, please install the chart on the same namespace where you installed Polyaxon.

```yaml
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

## Polyaxon's charts repo

You can add the Polyaxon helm repository to your helm, so you can install Polyaxon and other charts provided by Polyaxon from it. 
This makes it easy to refer to the chart without having to use a long URL each time.

## Install the nfs provisioner

```yaml
helm install polyaxon/nfs-provisioner --name=plx-nfs --namespace=polyaxon
```

## Configuration

To enable the outputs with default values:

```yaml
outputs:
  size: 100Gi
  enabled: true
```

To enable the outputs with custom values:


```yaml
outputs:
  enabled: true
```

Full reference:


| Parameter                | Description                                       | Default
| ---------------------    | ------------------------------------------------- | ----------------------------------------------------------
| `outputs.name`           | Name of the PVC to create                         | `polyaxon-pvc-outputs`
| `outputs.size`           | Size of outputs volume                            | `10Gi`
| `outputs.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


## Now you can use the PVC to mount outputs to your experiments and jobs in Polyaxon

```yaml
outputs:
  plx-outputs:
    existingClaim: polyaxon-pvc-outputs
    mountPath: /plx-outputs
```
