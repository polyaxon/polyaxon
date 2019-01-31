---
title: "Private Docker Registry"
meta_description: "How to pull images from your private docker registry."
custom_excerpt: "Use your secured, private, and internal docker registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
image: "../../content/images/integrations/docker.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - registry
featured: true
visibility: public
status: published
---

## Overview

You can easily add amany private registries to Polyaxon to pull private images and use them when scheduling your deep learning and machine learning experiments on Kubernetes using Polyaxon.

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
