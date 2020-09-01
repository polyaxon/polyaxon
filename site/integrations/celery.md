---
title: "Celery Scheduler"
meta_title: "Celery"
meta_description: "Polyaxon comes with a celery scheduler that can be enabled for scaling and processing background tasks."
custom_excerpt: "Celery beat is a scheduler; It kicks off tasks at regular intervals, that are then executed by available worker nodes in the cluster."
image: "../../content/images/integrations/celery.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
featured: false
popularity: 1
class_name: instruction
visibility: public
status: published
---

Polyaxon comes with a Celery scheduler that can be enabled for scaling and processing background tasks.
The Celery scheduler is disabled by default, we suggest that most users should first try to scale and tune the API first,
and then enable the schedule if they feel that it will bring more performance to their system.

the Celery scheduler can be enabled if:
  * Your deployment expects a large number of operations.
  * You are using Polyaxon SDKs to consume events from an external system and start jobs programmatically.

## Enable a broker

In order to use the scheduler you need to enable a [broker](/docs/setup/platform/broker/), Polyaxon provides two options for that:

 * [Redis](/docs/setup/platform/redis-ha/)
 * [Rabbitmq](/docs/setup/platform/rabbitmq-ha/)


## Enable the scheduler

You can now enable the scheduler and optionally change the default values:

```yaml
scheduler:
  enabled: true
  ...
```

## Tune the Celery configuration

Polyaxon provides several options for tuning Celery, please check this [guide](/docs/setup/platform/celery/).
