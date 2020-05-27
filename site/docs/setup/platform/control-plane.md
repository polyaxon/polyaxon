---
title: "EE control plane setup"
sub_link: "platform/control-plane"
meta_title: "Polyaxon control plane setup - Configuration"
meta_description: "Polyaxon control plane setup."
tags:
    - configuration
    - polyaxon
    - kubernetes
sidebar: "setup"
---

> If you are looking for the open-source setup, please check this [guide](/docs/setup/platform/open-source/).

## Polyaxon EE Control Plane

When deploying Polyaxon as a control plane to manage agent deployments, you need to set some extra configuration.

## Root user

The default superuser/root user for polyaxon.
You can set a password or a random password will be generated that you can retrieve later.

```yaml
user:
  username: "root"
  email: "root@polyaxon.local"
  password: "rootpassword"
```

## Disable agent services

Since some services will be managed by Polyaxon Agents on each cluster/namespace you don't need the default agent deployed:

```yaml
operator:
  enabled: false
streams:
  enabled: false
```

## Enable extra services

Some services are only available to Polyaxon control plane:

```yaml
redis:
  enabled: true
scheduler:
  enabled: true
worker:
  enabled: true
beat:
  enabled: true
```

> **Note**: You can have more control about the broker, please check this [guide](/docs/setup/platform/broker/).


## Admin view

To enable the DB admin interface:

```yaml
adminViewEnabled: true
```

## Connections

Remove all configuration related to connections, each agent will be managing its own connections.

```yaml
artifactsStore: {}
connections: []
notificationConnections: []
```
