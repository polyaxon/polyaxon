---
title: "Multiarch Deployment"
sub_link: "deployment-strategies/multiarch"
title_link: "Multiarch Deployment"
meta_title: "How to deploy Polyaxon on Kubernetes with CPU-heterogeneous node architecture."
meta_description: "This is a guide to assist you through the process and strategies of deploying Polyaxon on Kubernetes with CPU-heterogeneous node architecture."
tags:
  - setup
  - kubernetes
  - install
sidebar: "setup"
---

## Overview

Oftentimes, teams deploying Polyaxon on-premise might face CPU-heterogeneity of their compute nodes, i.e. a mixture of node architecture amd64, ppc64le, others.

The default images shared on docker-hub are amd64, which means that the containers scheduled on the ppc64le nodes during the experimentation or build stage will fail.

## Enable the multiarch image tag

Polyaxon provides multiarch docker manifests for its core components, which allows to deploy Polyaxon and schedule experiments on the entire cluster, independently of the node architecture.

Every Polyaxon component shared on dockerhub gets released with two tags: `release-tag` and `multiarch-release-tag`, e.g. `polyaxon/polyaxon-api:1.x.x` and `polyaxon/polyaxon-api:multiarch-1.x.x`.

## Changing the deployment config file

You need to override the default tag that comes with the Polyaxon version you are deploying, for instance, if you are deploying Polyaxon v1.x.x,
all images will be using a tag: `1.x.x`, in the deployment config file you need to override that value with `multiarch-1.x.x`:

```yaml
scheduler:
  imageTag: multiarch-1.x.x
gateway:
  imageTag: multiarch-1.x.x
init:
  imageTag: multiarch-1.x.x
sidecar:
  imageTag: multiarch-1.x.x
```
