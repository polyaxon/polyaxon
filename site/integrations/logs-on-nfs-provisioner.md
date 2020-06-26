---
title: "Logs on NFS Provisioner"
meta_title: "NFS Provisioner"
meta_description: "Using logs on an NFS server provisioner in your Polyaxon experiments and jobs. This integration simplifies the creation of ReadWriteMany and ReadOnlyMany volumes."
custom_excerpt: "Polyaxon in-cluster NFS provisioner to simplify the creation of ReadWriteMany and ReadOnlyMany volumes."
image: "../../content/images/integrations/nfs-provisioner.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - logging
  - storage
featured: false
popularity: 0
visibility: public
status: published
---

Polyaxon in-cluster NFS provisioner to simplify the creation of ReadWriteMany and ReadOnlyMany volumes.


## Overview

This guide shows how to use the NFS provisioner to mount logs to your jobs and experiments. 

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

To enable the logs with default values:

```yaml
logs:
  size: 100Gi
  enabled: true
```

To enable the logs with custom values:


```yaml
logs:
  enabled: true
```

Full reference:


| Parameter             | Description                                       | Default
| --------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `logs.name`           | Name of the PVC to create                         | `polyaxon-pvc-logs`
| `logs.size`           | Size of logs volume                               | `10Gi`
| `logs.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


## Now you can use the PVC to mount logs to your experiments and jobs in Polyaxon

```yaml
logs:
  existingClaim: polyaxon-pvc-logs
  mountPath: /plx-data
```
