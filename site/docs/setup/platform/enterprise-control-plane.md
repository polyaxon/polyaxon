---
title: "Enterprise Edition Control Plane Setup"
sub_link: "platform/enterprise-control-plane"
meta_title: "Polyaxon Enterprise Edition Control Plane Setup - Configuration"
meta_description: "Polyaxon Enterprise Edition Control Plane Setup."
tags:
  - configuration
  - polyaxon
  - kubernetes
sidebar: "setup"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

This guide is for Polyaxon Enterprise Edition Control Plane Setup for Kubernetes.

In order to deploy Polyaxon Enterprise Control Plane to manage agent deployments, you need to set some extra configuration.

## Set the EE License

Running Polyaxon Enterprise Control Plane requires a valid license.

As part of the sign-up process for Polyaxon EE, you should have received a license file.
If you do not have one, please contact us.
Save the license file temporarily to disk with filename license (no file extension) and execute the following:

```bash
kubectl create secret generic polyaxon-enterprise-license --from-file=./license -n polyaxon
```

## Configure Polyaxon Enterprise Docker registry access

Set up Docker credentials to allow Kubernetes nodes to pull down the Polyaxon Enterprise Docker images,
which are hosted in a private repository.
You receive credentials for the Polyaxon Enterprise Docker image when you sign up for Polyaxon Enterprise.

```bash
kubectl create secret -n polyaxon docker-registry polyaxon-docker-enterprise-k8s \
    --docker-server=<polyaxon-docker-enterprise-k8s-server> \
    --docker-username=<your-username> \
    --docker-password=<your-api-key>
```

## Add your organization key

```yaml
api:
  organizationKey: ...
```

## Use Polyaxon Enterprise Docker images

You need to set your configuration file to use Polyaxon Enterprise Docker images.

```yaml
api:
  image: ...
scheduler:
  image: ...
compiler:
  image: ...
worker:
  image: ...
beat:
  image: ...
```

## Disable the default agent services

Since some services will be managed by Polyaxon Agents on each cluster/namespace you don't need the default agent deployed:

```yaml
agent:
  enabled: false
operator:
  enabled: false
```

## Enable the scheduler

Polyaxon control plane requires the scheduler to be running. e.g. using redis:

```yaml
broker: redis
redis:
  enabled: true
scheduler:
  enabled: true
```

> **Note**: You can have more control about the broker, please check this [guide](/docs/setup/platform/broker/).

## Enable extra services

Some services are only available to Polyaxon control plane:

```yaml
compiler:
  enabled: true
worker:
  enabled: true
beat:
  enabled: true
```

## Connections

Remove all configuration related to connections, each agent will be managing its own connections and artifacts store.

```yaml
artifactsStore: {}
connections: []
```
