---
title: "Private registries"
sub_link: "private-registries"
meta_title: "Integrate your private docker images and registries in Polyaxon - Configuration"
meta_description: "Polyaxon allows to define and pull images from private Container Registries."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
    - environment
    - orchestration
    - registries
    - gcr
    - ecr
    - acr
    - docker
sidebar: "configuration"
---

<blockquote class="warning">This configuration is only available for Polyaxon deployed on Kubernetes clusters.</blockquote>

Polyaxon allows to pull and push images from private Container Registries.

By default Polyaxon ships with a Docker Registry which is included in the system namespace. 
Since this docker registry is running inside your kubernetes cluster and is used internally inside your cluster.

## Using a different Docker Registry

If you are using the public cloud you may wish to take advantage of your cloud providers docker registry; or reuse your own existing docker registry.

### Disable the build Docker Registry

In your deployment config yaml file:

```yaml
docker-registry:
  enabled: false
```

### Create a secret containing your auth credentials

You need to create a secret containing docker credentials config, e.g.

```json
{
    "auths": {
        "localhost:5001": {
            "auth": "YW11cmRhY2E6c3VwZXJzZWNyZXRwYXNzd29yZA==",
            "email": "user@acme.com"
        }
    },
    "credsStore": "secretservice"
}
``` 

Please see how you can integrate Polyaxon with different [cloud providers docker registries](/integrations/registry/).

### Add the access information to your registry catalog

After creating the secret with a docker credentials config authorizing access to one or many Docker registries, 
you need to add a new access to your Polyaxon's registries catalog:

![access](../../content/images/integrations/docker-access.png)

And you need to set the access as default one.  

## Pulling private images

If you want to keep using the built-in Docker Registry and authorize the [Native Builder](/integrations/native-build/) or [Kaniko](/integrations/kaniko/) to pull private images, 
you can follow the same steps as before to provide authentication to all registries the docker process should have access to, 
and leave the host to use the internal docker process, if the host is not provided and the build-in Docker Registry is disabled the builds will fail.
