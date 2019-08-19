---
title: "Amazon ECR"
meta_title: "Amazon ECR"
meta_description: "How to pull images from your private Amazon ECR registry. Use your Amazon ECR (elastic container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "Amazon Elastic Container Registry (ECR) is a fully-managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images."
image: "../../content/images/integrations/ecr.png"
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

You can use your docker images hosted on [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/).

## Overview

You can use your public images without the need to set any configuration. 

In order to use private images hosted on ECR, you need to grant the build access. 

## Create a secret containing the credentials to use with ECR

```json
{
    "credsStore": "ecr-login"
}
```

```bash
kubectl create secret generic docker-conf --from-file=config.json=./config.json -n polyaxon
```

## Add the secret to the k8s_secrets catalog in Stores

In order to use secret that you created before, in Polyaxon's Stores > Secrets, create a new secret entry, and set name and K8S Ref to "docker-conf".

## Create a docker registry access in the UI

In Polyaxon's stores, add a new entry and link to this secret, and set the host to your ECR.

![access](../../content/images/integrations/docker-access.png)


## Make this access as default

After creating the access you need to mark it as default, so that Polyaxon uses it for scheduling builds. 


## Using the secret for pull only

If you wish to only use this credential secret for pulling images and the in-cluster registry for pushing, you should leave the host field empty.

## You can allow the docker process to pull from different registries

To allow this access to pull from other registries, you can set as many other auths and credsStore.
