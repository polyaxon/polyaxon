---
title: "Artifacts on NFS Provisioner"
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
  - artifacts
  - storage
featured: false
popularity: 0
visibility: public
status: published
---

Polyaxon in-cluster NFS provisioner to simplify the creation of ReadWriteMany and ReadOnlyMany volumes.


## Install Helm

To install the nfs-provisioner, make sure you have [Helm](https://helm.sh/docs/intro/install/) installed.


## Create Namespace

If you are using this chart with Polyaxon, please install the chart on the same namespace where you installed Polyaxon.

```bash
kubectl create namespace polyaxon

# namespace "polyaxon" created
```

## Install the nfs provisioner

```yaml
helm install plx-nfs stable/nfs-server-provisioner --namespace=polyaxon
```

Create volumes to be used as [artifacts store](https://github.com/bitnami/charts/tree/main/bitnami/nfs-server-provisioner#recommended-persistence-configuration-examples).

## Use the PVC as an artifacts store in Polyaxon

In order to use the PVC with Polyaxon, you can follow the [artifacts on Persistent Volume Claim](/integrations/data-on-pvc/).
