---
title: "Amazon ECR"
meta_title: "Amazon ECR"
meta_description: "How to pull images from your private Amazon ECR registry. Use your Amazon ECR (elastic container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "Amazon Elastic Container Registry (ECR) is a fully-managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images."
image: "../../content/images/integrations/ecr.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - registries
  - aws
featured: false
popularity: 0
visibility: public
status: published
---

You can use your docker images hosted on [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/).

## Overview

You can use your public images without the need to set any configuration.
In order to push private images to ECR, you need to grant the build access.

## Kaniko

In order to push docker images to ECR, please follow this [guide](https://github.com/GoogleContainerTools/kaniko#pushing-to-amazon-ecr) for configuring a registry to use with Kaniko.

If you decide to use the secret and config-map approach, your connection should be:

```yaml
connections:
  - name: docker-registry
    kind: registry
    description: "aws docker repository"
    schema:
      url: aws_account_id.dkr.ecr.region.amazonaws.com
    secret:
      name: aws-secret
      mountPath: /root/.aws/
```
