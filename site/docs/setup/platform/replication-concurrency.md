---
title: "Replication & Concurrency"
sub_link: "platform/replication-concurrency"
meta_title: "Replication and Concurrency in Polyaxon - Configuration"
meta_description: "Polyaxon supports scaling of it's services (API and workers) in a horizontal way using replication, and the user can increase the workers' concurrency for higher throughput."
tags:
  - configuration
  - polyaxon
  - replication
  - scaling
  - concurrency
  - kubernetes
  - docker-compose
sidebar: "setup"
---

Polyaxon supports scaling of it's services (API and workers) in a horizontal way using replication, and the user can increase the workers' concurrency for higher throughput.

## Services Replication

To replicate the platform or one of the services (API or workers),
you just need to modify the `replicas` field of that service you want to scale horizontally.

> There's an hpa for horizontal pod auto-scaling that can be enabled for all services

## Gateway

```yaml
gateway:
  replicas: 3
```

## Scheduler

```yaml
scheduler:
  replicas: 3
```

## Worker

```yaml
worker:
  replicas: 3
```

## Concurrency

Replication might be easier to scale Polyaxon, but it comes at a memory cost, as it's not always efficient,
Polyaxon provides a way to scale it's services' concurrency as well,
the rule of thumb is to set the concurrency of the worker you wish to scale to the number of cores available.
This will allow to reduce the memory footprint on your cluster and allow the worker to consume more events/tasks.

For example you may want to increase the concurrency of the scheduler:

```yaml
scheduler:
  replicas: 2
  concurrency: 10
worker:
  replicas: 2
  concurrency: 5
```

This will create 2 replicas for the scheduler, with 10 concurrent processes each.

## Operator

Increasing the operator's concurrent reconciles

```yaml
operator:
  maxConcurrentReconciles: 8
```
