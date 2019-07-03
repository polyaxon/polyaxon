---
title: "Google GCR"
meta_title: "Google GCR"
meta_description: "How to pull images from your private Google GCR registry. Use your Google GCR (Google container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "Google Container Registry is is a fully-managed Docker container registry to store, manage, and secure your Docker container images."
image: "../../content/images/integrations/gcr.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - registry
featured: false
visibility: public
status: published
---

Integrate your Google GCR (Google container registry) with Polyaxon to start your machine learning and deep learning experiments on Kubernetes.

## Overview

You can easily add many private registries to Polyaxon to pull private images and use them when scheduling your deep learning and machine learning experiments on Kubernetes using Polyaxon.

## Create a secret containing the credentials to use with GCR

You can use the `privateRegistries` section to set your Google container registry authentication:

```bash
kubectl create secret generic docker-conf --from-file=config.json=./config.json -n polyaxon
```

N.B. you can also create a secret based on the authentication:

```
user: "_json_key"
password: '{"type": "service_account", "project_id": "my_project", "private_key_id": "ajshvasjhqweqetquytqut17253871238", "private_key": "-----BEGIN PRIVATE KEY-----\nASBHJASJDASBDJAJHSBDJB/sfbdj1223"}'
```

## Create a docker registry access in the UI

In Polyaxon's stores, add a new entry and link to this secret, and set the host to gcr.io, us.gcr.io, eu.gcr.io, or asia.gcr.io.

![access](../../content/images/integrations/docker-access.png)


## Make this access as default

After creating the access you need to mark it ass default, so that Polyaxon uses it for scheduling builds. 


## Using the secret for pull only

If you wish to only use this credential secret for pulling images and the in-cluster registry for pushing, you should leave the host field empty.

## You can include allow the docker process to pull from different registries

To allow this access to pull from other registries, you can set as many other auths and credsStore.
