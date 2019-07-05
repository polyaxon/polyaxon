---
title: "Native builder"
meta_title: "Native builder"
meta_description: "Polyaxon allows users to build container images using the native builder project."
custom_excerpt: "Polyaxon native builder is a Python library for the Docker Engine API."
image: "../../content/images/integrations/native-builder.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - containers
  - scheduling
featured: false
visibility: public
status: published
---

Polyaxon allows users to build container images in-cluster before stating experiment and jobs.

### Overview

Polyaxon supports multiple backend options to build container images used for running jobs or training experiments.

The native builder is a lightweight container builder, and it's the default backend used in Polyaxon deployment, it has been tested and works smoothly.

If you have changed the default build backend, and you need to use the native builder for some use cases you can follow one of the following options.

> If your builds fail in EKS clusters it could be due to DNS resolution, please see this [issue](https://github.com/awslabs/amazon-eks-ami/issues/183). 
> The builds are failing because the latest versions of the AWS EKS-optimized AMI disables the docker bridge network by default. 
> To enable it, add the `bootstrap_extra_args` parameter to your worker group template.

> ```
> locals {
>   worker_groups = [
>     {
>       # Other parameters omitted for brevity
>       bootstrap_extra_args = "--enable-docker-bridge true"
>     }
>   ]
> }
> ```

## Using the native builder per job/experiment

In case the default build backend is the not the native builder, 
users who want to use this native builder to build container images must define explicitly the backend option in their Polyaxon files:

```yaml
...
build:
  ...
  backend: native
```

## Using the native builder as the default build backend

In order to use the native build backend as the default builder option in Polyaxon, users need to either remove or set `build backend` option in the settings page in the dashboard to

```yaml
native
```

By deleting this option as well, you are using the default values, and the native build backend is one of them.
