---
title: "Docker Hub"
meta_title: "Docker Hub Registry"
meta_description: "How to pull images from your private docker hub registry."
custom_excerpt: "Docker Hub is a service provided by Docker for finding and sharing container images with your team. Docker Hub is the world's largest library and community for container images"
image: "../../content/images/integrations/dockerhub.png"
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

You can use your docker images hosted on [https://hub.docker.com/](https://hub.docker.com/).


## Overview

You can use your public images without the need to set any configuration. 

In order to use private docker images hosted on docker hub, you need to set access credentials. 

## Create a secret containing the credentials to use with docker hub

```json
{
    "auths": {
        "https://index.docker.io/v1/": {
            "auth": "YW11cmRhY2Esdfdsflkdjsf==",
            "email": "user@acme.com"
        }
    }
}
```

or 

```json
{
    "auths": {
        "https://index.docker.io/v1/": {
            "auth": "YW11cmRhY2Esdfdsflkdjsf=="
        }
    }
}
```

N.B. that the auth must contain a concatenation of the username, a colon, and the password, i.e. `user:password`, 
you can find the auths in your `$HOME/.docker/config.json` for instance, or you can create this auth using a simple python script:

```python
import base64
base64.b64encode("user:secret".encode())
```

```bash
kubectl create secret generic docker-conf --from-file=config.json=./config.json -n polyaxon
```

## Add the secret to the k8s_secrets catalog in Stores

In order to use secret that you created before, in Polyaxon's Stores > Secrets, create a new secret entry, and set name and K8S Ref to "docker-conf".

## Create a docker registry access in the UI

In Polyaxon's stores, add a new entry and link to this secret, and set the host to `https://index.docker.io/v1/`.

![access](../../content/images/integrations/docker-access.png)


## Make this access as default

After creating the access you need to mark it as default, so that Polyaxon uses it for scheduling builds. 


## Using the secret for pull only

If you wish to only use this credential secret for pulling images and the in-cluster registry for pushing, you should leave the host field empty.

## You can allow the docker process to pull from different registries

To allow this access to pull from other registries, you can set as many other auths and credsStore.
