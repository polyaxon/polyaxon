---
title: "Private Docker Registry"
meta_title: "Docker Registry"
meta_description: "How to pull images from your private docker registry. Use your secured, private, and internal docker registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "The Docker Registry for storing and distributing Docker images."
image: "../../content/images/integrations/docker.png"
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

## Overview

You can easily add many private registries to Polyaxon to pull private images and use them when scheduling your deep learning and machine learning experiments on Kubernetes using Polyaxon.

## Add your private docker registry to the Polyaxon deployment config

Now you can use the `privateRegistries` section to set your private docker registry information:

```yaml
privateRegistries:
  - "my_username:my_password@registry.example.com"
```

or 

```yaml
privateRegistries:
  - host: "another.registry.com"
    user: "myname"
    password: "mypassword"
```
