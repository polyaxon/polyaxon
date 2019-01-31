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

Polyaxon allows to define and pull images from private Container Registries.

As an example, let's assume that you want to use the `registry.example.com/private/image:v1.1` image
which is private and requires you to login into a private container registry.

Let's also assume that these are the login credentials:

Key | value
-------|------
  registry| registry.example.com
  username| my_username
  password| my_password

To configure access for `registry.example.com`, you need to add the registry to your configuration based on our URI spec:

`"user:passowrd@host:port"` or `"user:passowrd@site.com"`

In the case of the example you need to add your container registry to deployment configuration:

```yaml
privateRegistries:
  - "my_username:my_password@registry.example.com"
```

Polyaxon will turn this uri specification into a secret and expose it to the necessary service
responsible for building your experiment/job images.

You can have more than one private container registry defined in your Polyaxon deployment configuration:

```yaml
privateRegistries:
  - "my_username:my_password@registry.example.com"
  - "my_username2:my_password2@registry:5000"
```

Although the uri spec is the preferred way for defining private registries, 
Polyaxon supports dictionaries as well, users can use both approaches to define private registries:


```yaml
privateRegistries:
  - "my_username:my_password@registry.example.com"
  - "my_username2:my_password2@registry:5000"
  - host: "my.registry.com"
    user: "_json_key"
    password: '{"type": "service_account", "project_id": "my_project", "private_key_id": "ajshvasjhqweqetquytqut17253871238", "private_key": "-----BEGIN PRIVATE KEY-----\nASBHJASJDASBDJAJHSBDJB/sfbdj1223"}'
  - host: "another.registry.com"
    user: "myname"
    password: "mypassword"
```
