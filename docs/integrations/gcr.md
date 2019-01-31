---
title: "Google GCR"
meta_description: "How to pull images from your private Google GCR registry."
custom_excerpt: "Use your Google GCR (Google container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
image: "../../content/images/integrations/gcr.png"
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

Now you can use the `privateRegistries` section to set your Google container registry authentication:

```yaml
privateRegistries:
  - host: "my.registry.com"
    user: "_json_key"
    password: '{"type": "service_account", "project_id": "my_project", "private_key_id": "ajshvasjhqweqetquytqut17253871238", "private_key": "-----BEGIN PRIVATE KEY-----\nASBHJASJDASBDJAJHSBDJB/sfbdj1223"}'

```
