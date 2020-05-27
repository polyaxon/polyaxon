---
title: "Kaniko"
meta_title: "Kaniko"
meta_description: "Polyaxon allows users to build container images using the Kaniko project."
custom_excerpt: "kaniko is a tool to build container images from a Dockerfile, inside a container or Kubernetes cluster."
image: "../../content/images/integrations/kaniko.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - containers
  - scheduling
featured: true
visibility: public
status: published
---

Polyaxon allows users to build container images using the Kaniko project.

### Overview

Polyaxon supports multiple backend options to build container images used for running jobs or training experiments.

You can configure Kaniko as a build backend per job/experiment or as the default build backend.  

## Using Kaniko per job/experiment

In case the default build backend is not Kaniko, 
users who want to use Kaniko to build container images must define explicitly the backend option in their Polyaxon files:

```yaml
...
build:
  ...
  backend: kaniko
```

## Using Kaniko as the default build backend

In order to use Kaniko as the default backend build option in Polyaxon, users need to set `build Backend` option in the settings page in the dashboard to:

```yaml
kaniko
```

## Changing the Kaniko image, image tag, and the image pull policy

You can also change the default image and version used for creating the Kaniko build container in the settings page:

image:
```yaml
gcr.io/kaniko-project/executor:latest
```

imagePullPolicy:
 
```yaml
IfNotPresent
```
