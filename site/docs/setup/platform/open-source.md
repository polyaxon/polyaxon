---
title: "Open source setup"
sub_link: "platform/open-source"
meta_title: "Polyaxon Open source setup - Configuration"
meta_description: "Polyaxon Open source setup."
tags:
    - configuration
    - polyaxon
    - kubernetes
sidebar: "setup"
---

<blockquote class="warning">
The open-source distribution for this version is not published yet! Please join the <a href="/slack/">chat</a> for more details.
</blockquote>

## Polyaxon open-source

Polyaxon open-source deploys on a single cluster and a single namespace, there's no limitation on the number of nodes you can use.
The deployment comes with an in-cluster agent deployment for managing workload.

## Enable agent services

The open-source version manages the operator and the streams in a single deployment:

```yaml
operator:
  enabled: true
streams:
  enabled: true
```

## Enable extra services

If you wan to run Polyaxon with a scheduler to process tasks in an asynchronous fashion.

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
notificationConnections: []
```

You need to configure the connection to authorize for the platform. Please check [connections section](/docs/setup/connections/).
