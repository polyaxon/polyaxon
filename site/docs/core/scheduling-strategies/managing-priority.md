---
title: "Managing Priority"
sub_link: "scheduling-strategies/managing-priority"
meta_title: "Managing Priority - scheduling strategies"
meta_description: "Prioritize important operations and enforcing preemption."
visibility: public
status: published
tags:
  - tutorials
  - concepts
sidebar: "core"
---

## Overview

Polyaxon provides two features to prioritize work:
 * Queue priority
 * Kubernetes scheduler priority
 
## Queue Priority

Polyaxon allows to define a priority on each queue. The priority of a queue dictates how fast will Polyaxon move your operations from the that queue and pass it to Kubernetes relative to other queues defined under each agent.
For example, you may want put a Notebook operation or a debug operation on a priority queue while you may want to put a large hyperparameter search on a lower priority queue.

To use the queue priority feature, you need to define multiple queues with different priorities and you need to use the `queue` field to assign operations to queues.

## Kubernetes scheduler priority

Kubernetes allows to run workloads with relative priorities. This give users a second layer to control how Kubernetes should behave when several operations are moved from Polyaxon's queues to Kubernetes.
This is useful when some operations need to acquire resources faster than others.
For example, you may want to schedule a notebook service to acquire a node before a long training job.

To set Kubernetes priority on an operation, you need to set the fields [priority](/docs/core/specification/environment/#priority) and/or [priority_class_name](/docs/core/specification/environment/#priorityclassname).

