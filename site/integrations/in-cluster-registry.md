---
title: "In-Cluster Registry"
meta_title: "In-Cluster Kubernetes Registry"
meta_description: "How to create and push images to an in-cluster Kubernetes docker registry."
custom_excerpt: "Docker Registry Helm Chart is a private Docker Registry deployed ina kubernetes cluster."
image: "../../content/images/integrations/dockerhub.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - registries
featured: false
popularity: 0
visibility: public
status: published
---

This guide describes how to install an in-cluster docker registry in Kubernetes, using the standard Helm charts.

## Overview

A local docker registry can be used to push container images directly to the cluster, which could be useful for example in the following cases:
 * Your jobs have no Internet access, so container images cannot be downloaded directly from an external registry.
 * You are iterating on new experiments and you want to test your changes before uploading the image to the official docker repository.

> **Note**: Insecure registries can be used for development and trials. 
 You should not use this in production. To deploy a secure registry, please consider customizing the chart or use an external registry provider.

## Deploy a docker registry using Helm

We will deploy an insecure registry on a Kubernetes cluster using the official Helm chart.

```bash
helm install polyaxon-containers stable/docker-registry --set service.nodePort=30500,service.type=NodePort -n docker-registry
```

> You can exposes the registry on a different port.


## Add catalog connections 

If you want to build images using Kaniko component:

```yaml
  - name: docker_connection
    kind: registry
    schema:
      url: "polyaxon-containers-docker-registry.docker-registry.svc.cluster.local:5000"
```

If you want to build images using the Dockerizer component:

```yaml
  - name: docker_connection_dockerizer
    kind: registry
    schema:
      url: "127.0.0.1:30500"
```

You can add both connections to your catalog if you intend to try both components.
