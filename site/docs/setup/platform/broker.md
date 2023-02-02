---
title: "Async Workers Broker configuration"
sub_link: "platform/broker"
meta_title: "Asynchronous Workers Broker in Polyaxon - Configuration"
meta_description: "Polyaxon's Asynchronous Workers Broker configuration."
tags:
  - configuration
  - polyaxon
  - kubernetes
  - broker
sidebar: "setup"
---

Polyaxon comes with a built-in queue to process tasks in a more asynchronous fashion.

For example when a new event comes in instead of writing it to the database immediately,
it schedules a task to the queue so that the request can be returned right away,
and the background workers handle saving that data.

> By default, Polyaxon does not deploy with a broker enabled.


## RabbitMQ

If you run with a high workload, or have concerns about fitting the pending workload in memory,
then RabbitMQ is an ideal candidate for backing Polyaxon’s asynchronous workers.

```yaml
rabbitmq:
  enabled: true
```

You can have as much control on the RabbitMQ dependency, or you can [turn it off and provide your own instance configuration](/docs/setup/platform/postgresql-ha/).


## Redis

Redis can be used and will work in most situations.
The primary limitation of using Redis is that all pending work must fit in memory.

In order to use Redis as the broker, make sure to disable RabbitMQ (to not waste resources), and set `broker` option to redis:

```yaml
redis:
  enabled: true

broker: redis
```

You can further customize the redis dependency or you can [turn it off and provide your own instance configuration](/docs/setup/platform/redis-ha/).
