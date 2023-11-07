---
title: "Community Edition Setup"
sub_link: "platform/community-edition"
meta_title: "Polyaxon Community Edition Setup - Configuration"
meta_description: "Polyaxon Community Edition Setup based on Polyaxon open-source."
tags:
  - configuration
  - polyaxon
  - kubernetes
sidebar: "setup"
---

## Overview

Polyaxon Community Edition is based on Polyaxon's [open-source project](https://github.com/polyaxon/polyaxon),
and it deploys on a single cluster and a single namespace, there's no limitation on the number of nodes you can use.
The deployment comes with an in-cluster agent deployment for managing workload.

The best way to deploy and try Polyaxon is to keep the default `ClusterIp` service type,
and use `polyaxon port-forward` command to expose the API and dashboard on your localhost in a secure way,
the command will auto-configure the client and the cli for future interactions:

```bash
polyaxon admin deploy ...
polyaxon port-forward
```

If you wish to expose your Polyaxon deployment to several users, each user can port-forward the traffic to localhost,
or you can also spend some time to configure a load balancer or ingress.

## Enable agent services

Polyaxon Community Edition manages the operator and the gateway in a single deployment, and they must be enabled, please do not disable these services:

> **Note**: This is the default configuration of the chart, you do not need to add this to your deployment config file.

```yaml
operator:
  enabled: true
```

## Enable extra services

Polyaxon API can be easily scaled horizontally if you have a growing traffic,
but you are submitting a large number of operations, and you think that you can benefit from using a background worker,
you can enable the open-source scheduler to process events and submission in an asynchronous fashion.

> **Note**: By default, the scheduler is disabled, you should only enable it after scaling the API service.

```yaml
redis:
  enabled: true
scheduler:
  enabled: true
```

> **Note**: You can have more control about the broker, please check this [guide](/docs/setup/platform/broker/).

## Connections

```yaml
artifactsStore: {}
connections: []
```

You need to configure the connections to authorize for the platform. Please check [connections section](/docs/setup/connections/).

## Community UI

The community UI is an optional free tool that can be used to view information about your jobs and services,
it's enabled by default for all deployments.

If your main use of Polyaxon is to schedule jobs, use the packaging format, and interact with the platform using the CLI/Client/APIs,
you can disable the UI:

```yaml
ui:
  enabled: false
```

## Security

Polyaxon will deploy by default using a ClusterIp service, and provides a command to port-forward the traffic to localhost in a secure way.
If you decide to deploy Polyaxon CE using a LoadBalancer or an Ingress,
we strongly recommend that users only use environments they control by locking the deployment down at the network level.
