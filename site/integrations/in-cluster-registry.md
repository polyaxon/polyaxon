---
title: "In-Cluster Registry"
meta_title: "In-Cluster Kubernetes Registry"
meta_description: "How to create and push images to an in-cluster Kubernetes docker registry."
custom_excerpt: "Docker Registry Helm Chart is a private Docker Registry deployed ina kubernetes cluster."
image: "../../content/images/integrations/docker.png"
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

This guide describes how to use an in-cluster docker registry in Kubernetes with Polyaxon to build containers.

<blockquote class="info">
This <a href="https://www.linuxtechi.com/setup-private-docker-registry-kubernetes/">blog post</a> shows how to deploy an in-cluste registry.
Note that this tutorial does not show how to mount a PVC to store the images, this tutorial is not meant to be a production environment.
</blockquote>

## Overview

A local docker registry can be used to push container images directly to the cluster, which could be useful for example in the following cases:
 * Your jobs have no internet access, so container images cannot be downloaded directly from an external registry.
 * You are iterating on new experiments and you want to test your changes before uploading the image to the official docker repository.

> **Note**: Insecure registries can be used for development and trials.
> You should not use this in production. To deploy a secure registry, please consider customizing the chart or use an external registry provider.

## Install the in-cluster registry

You can follow the [tutorial](https://www.linuxtechi.com/setup-private-docker-registry-kubernetes/) or you can use this starting manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: private-repository-k8s
  labels:
    app: private-repository-k8s
spec:
  replicas: 1
  selector:
    matchLabels:
      app: private-repository-k8s
  template:
    metadata:
      labels:
        app: private-repository-k8s
    spec:
      volumes:
        - name: registry-vol
          hostPath:
            path: /tmp
            type: Directory
      containers:
        - image: registry:2
          name: private-repository-k8s
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          volumeMounts:
            - name: registry-vol
              mountPath: /var/lib/registry
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: private-repository-k8s
  name: private-repository-k8s
spec:
  ports:
    - port: 5000
      nodePort: 31320
      protocol: TCP
      targetPort: 5000
  selector:
    app: private-repository-k8s
  type: NodePort
```

> **Note**: This is not a production manifest and you will need to adapt it. 

## Docker registry ports

You need to check the nodes that you expose for your in-cluster registry. In this guide we assume that:
 * The nodePort: `31320`
 * The targetPort: `5000`


## Add catalog connections

If you want to build images using Kaniko component:

```yaml
  - name: docker_connection
    kind: registry
    schema:
      url: "SERVICE_NAME.NAMESPACE.svc.cluster.local:5000"
```

If you want to build images using the Dockerizer component:

```yaml
  - name: docker_connection_dockerizer
    kind: registry
    schema:
      url: "127.0.0.1:31320"
```

You can add both connections to your catalog if you intend to try both components.
