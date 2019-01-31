---
title: "Amazon ECR"
meta_description: "How to pull images from your private Amazon ECR registry."
custom_excerpt: "Use your Amazon ECR (elastic container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
image: "../../content/images/integrations/ecr.png"
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
status: coming-soon
---

## Overview

You can easily add amany private registries to Polyaxon to pull private images and use them when scheduling your deep learning and machine learning experiments on Kubernetes using Polyaxon.

## Add your private docker registry to the Polyaxon deployment config

Now you can set the email section using your ECR registry information:

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
