---
title: "Concurrency Management"
sub_link: "scheduling-strategies/concurrency-management"
meta_title: "Managing concurrency and parallelism in Polyaxon - scheduling strategies"
meta_description: "A feature managing concurrency and controlling parallelism."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---


## Overview

Polyaxon has 3 levels of concurrency and parallelism management, each level serves a specific use case.

## Global organization limit

This is the highest concurrency limit you can achieve in your organization. This value depends on your subscription plan.
Every agent created has a default queue, we configure that default queue with unlimited concurrency to allow users to maximize their plan's usage.

We suggest that you always leave at least a single queue with the highest priority and unlimited concurrency.
If you are running a debug operation or need to see the results of an experiment quickly,
a queue with this configuration is very handy since it will prioritize your operation, and you will avoid being throttled.

## Queue parallelism

Queues are an organization/agent level abstraction to share and divide the global concurrency.
Queues can be used for several use cases: routing, prioritization, and parallelism throttling.
Additionally, if you need to limit the parallelism of a component globally, you can attach a queue to that component,
so whenever a new operation is referencing that component, it will be automatically throttled by the concurrency defined on that queue.

> for more details, please check the [Queues section](/docs/core/scheduling-strategies/queues/).

## Pipeline concurrency

Sometimes you will need to run a workflow, a mapping, or a hyperparameter tuning operation with a large search space or several independent operations.
Although it's possible to use queues to limit the concurrency of such pipelines,
it does not make sense to create a queue or change some queue's limit to fit the needs of each pipeline.

Polyaxon exposes a field concurrency on all abstractions that create pipelines, this field creates a short-lived queue to control the pipeline parallelism.

> for more details, please check the [automation concurrency section](/docs/automation/helpers/concurrency/)
