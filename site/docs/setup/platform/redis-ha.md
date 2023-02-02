---
title: "Redis HA"
sub_link: "platform/redis-ha"
meta_title: "High availability for Redis in Polyaxon - Configuration"
meta_description: "Polyaxon offers a couple of ways to set a high available redis instances."
tags:
  - configuration
  - polyaxon
  - redis
  - scaling
  - high-availability
  - kubernetes
  - docker-compose
sidebar: "setup"
---

Polyaxon ships with a default redis based on the stable [Helm chart](https://github.com/bitnami/charts/tree/main/bitnami/redis).

You can check the chart values to extend its configuration.

## External Redis

If you prefer to have Redis managed by you or hosted outside of Kubernetes,
you need to disable the in-cluster redis, and provide the information needed to establish a connection to the external one, e.g.:


```yaml
broker: redis

redis:
  enabled: false

externalServices:
  redis:
    password: polyaxon
    host: 35.262.163.88
```

## External Redis with password

If your redis instance requires a password, you need to provide it as well:


```yaml
broker: redis

redis:
  enabled: false

externalServices:
  redis:
    usePassword: true
    password: polyaxon
    host: 35.262.163.88
    port: 1234
```


### Memorystore for Redis

You can use [Cloud MemoryStore for Redis](https://cloud.google.com/memorystore/) if you are running Polyaxon on GKE,
please follow this [integration guide](/integrations/redis/).

## Using Redis as broker

You can also use Redis for as async worker broker, please check this section on how to alter the [default broker behavior](/docs/setup/platform/broker/).

## Scheduling

If you decided to deploy Redis in-cluster make sure to set proper [node scheduling](/docs/setup/platform/common-reference/#node-and-deployment-manipulation)
to avoid running high load runs on the same node hosting Redis.
