---
title: "Google GCR"
meta_title: "Google GCR"
meta_description: "How to pull images from your private Google GCR registry. Use your Google GCR (Google container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "Google Container Registry is is a fully-managed Docker container registry to store, manage, and secure your Docker container images."
image: "../../content/images/integrations/gcr.png"
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

Now you can use the `privateRegistries` section to set your Google container registry authentication:

```yaml
privateRegistries:
  - host: "my.registry.com"
    user: "_json_key"
    password: '{"type": "service_account", "project_id": "my_project", "private_key_id": "ajshvasjhqweqetquytqut17253871238", "private_key": "-----BEGIN PRIVATE KEY-----\nASBHJASJDASBDJAJHSBDJB/sfbdj1223"}'

```
