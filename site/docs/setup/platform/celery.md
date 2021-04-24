---
title: "Celery configuration"
sub_link: "platform/celery"
meta_title: "Celery Distributed Task Queue in Polyaxon - Configuration"
meta_description: "Polyaxon's Celery Distributed Task Queue configuration."
tags:
  - configuration
  - polyaxon
  - kubernetes
  - broker
  - celery
sidebar: "setup"
---

Polyaxon uses Celery for Distributed Task Queue.
This allows Polyaxon to execute tasks concurrently on a single or more worker servers.

Polyaxon exposes some configuration options to customize the behavior of the async workers.


## brokerPoolLimit

`Default: 10`

The maximum number of connections that can be open in the connection pool.

If set to None or 0 the connection pool will be disabled and connections will be established and closed for every use.


## confirmPublish

`default: True`

If you are using rabbitmq as a broker, this will guarantee message delivery.

## workerPrefetchMultiplier

`default: 4`

The prefetch limit is a limit for the number of tasks (messages) a worker can reserve for itself.
If it is zero, the worker will keep consuming messages, not respecting that there may be other available worker nodes that may be able to process them sooner,
or that the messages may not even fit in memory.


## workerMaxTasksPerChild

`default: None`

Maximum number of tasks a pool worker process can execute before it’s replaced with a new one. Default is no limit.

> **N.B.** setting this to a low value might have a negative impact on your workers since they will be replaced often.

## workerMaxMemoryPerChild

`default: 400000`

Maximum amount of resident memory, in kilobytes, that may be consumed by a worker before it will be replaced by a new worker.
If a single task causes a worker to exceed this limit, the task will be completed, and the worker will be replaced afterwards.

> **N.B.** setting this to a low value might have a negative impact on your workers since they will be replaced after a few tasks.
