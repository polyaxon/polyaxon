---
title: "Docker Registry Connections"
sub_link: "connections/registry"
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
sidebar: "setup"
---

Polyaxon allows to pull and push images from private container registries.

## Pulling docker image

If you only want to pull images from private registry,
you don't need to configure a registry connection,
you can use the [imagePullSecret](/docs/core/specification/environment/#imagepullsecrets)
field in the environment section.


## Schema Fields

### url

The url of the registry host.

```yaml
name: docker-connection-kaniko
kind: registry
schema:
  url: https://myregistry.com/org/repo
```

## Examples

### Example using a private registry with kaniko

```yaml
name: docker-connection-kaniko
kind: registry
schema:
  url: https://myregistry.com/org/repo
secret:
  name: docker-conf
  mountPath: /kaniko/.docker
```

### Example using a private registry with the dockerizer


```yaml
name: docker-connection-dockerizer
kind: registry
schema:
  url: https://myregistry.com/org/repo
secret:
  name: docker-conf
  mountPath: /root/.docker
```

In both example we are mounting the same secret but to 2 different paths,
if you are using the dockerizer for instance with a specific user
UID you might also want to change the path.


## Configuration

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

Please see how you can integrate Polyaxon with different [docker registry providers](/integrations/registries/).

### Add the access information to your connections catalog

After creating the secret with a docker credentials config authorizing access
to one or many Docker registries,
you need to add a new access to your connections catalog:

```yaml
connections:
  ...
  - name: my-docker-registry
    kind: registry
    description: some description
    schema:
      url: https://myregistry.com/org/repo
    secret:
      name: docker-conf
      mountPath: ...
```
