---
title: "Async Workers Broker configuration"
sub_link: "Asynchronous Workers Broker"
meta_title: "Asynchronous Workers Broker in Polyaxon - Configuration"
meta_description: "Polyaxon's Asynchronous Workers Broker configuration."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - broker
sidebar: "configuration"
---

Polyaxon comes with a built-in queue to process tasks in a more asynchronous fashion.

For example when a new event comes in instead of writing it to the database immediately, 
it schedules a task to the queue so that the request can be returned right away, 
and the background workers handle actually saving that data.

Prior to v0.5.0, Polyaxon supported one broker: RabbitMQ. 

Starting from v0.5.0, Polyaxon provides support for two primary brokers which may be adjusted depending on your workload: 
RabbitMQ and Redis.

 
## RabbitMQ (default option)

By default Polyaxon ships with a built-in RabbitMQ dependency which is used as the broker for scheduling asynchronous tasks.

If you run with a high workload, or have concerns about fitting the pending workload in memory, 
then RabbitMQ is an ideal candidate for backing Polyaxon’s asynchronous workers.

You can have as much control on the RabbitMQ dependency, or you can [turn it off and provide your own instance configuration](/configuration/rabbitmq-ha/).


## Redis

Redis can be used and will work under most situations. 
The primary limitation to using Redis is that all pending work must fit in memory.

In order to use Redis as the broker, make sure to disable RabbitMQ (to not waste resources), and set `broker` option to redis:

```yaml
rabbitmq-ha:
  enabled: false
  
broker: redis
```

You can further customize the redis dependency or or you can [turn it off and provide your own instance configuration](/configuration/redis-ha/).
