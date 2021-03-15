---
title: "Docker Hub"
meta_title: "Docker Hub Registry"
meta_description: "How to pull images from your private docker hub registry."
custom_excerpt: "Docker Hub is a service provided by Docker for finding and sharing container images with your team. Docker Hub is the world's largest library and community for container images"
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
popularity: 1
visibility: public
status: published
---

You can use your docker images hosted on [https://hub.docker.com/](https://hub.docker.com/).


## Overview

You can use your public images without the need to set any configuration.
In order to push private docker images to docker hub, you need to set access credentials.

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
you can find the auths in your `$HOME/.docker/config.json` for instance, or you can create this auth using a simple Python script:

```python
import base64
base64.b64encode("user:secret".encode())
```

```bash
kubectl create secret generic docker-conf --from-file=config.json=./config.json -n polyaxon
```

## Add the secret to the connections catalog

If you are using Kaniko

```yaml
  - name: docker-connection
    kind: registry
    schema:
      url: destination
    secret:
      name: docker-conf
      mountPath: /kaniko/.docker
```

If you are using dockerizer using the default root user:

```yaml
  - name: docker-connection-dockerizer
    kind: registry
    schema:
      url: destination
    secret:
      name: docker-conf
      mountPath: /root/.docker
```
