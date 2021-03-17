---
title: "Scheduling Strategies"
sub_link: "scheduling-strategies"
title_link: "Scheduling Strategies"
meta_title: "How to schedule runs on Polyaxon"
meta_description: "This is a guide to assist you through the process and strategies for scheduling your runs."
is_index: true
tags:
    - namespace
    - queueing
    - pipelines
    - kubernetes
    - scheduling
sidebar: "core"
---

## Overview

Oftentimes, teams will have several environments with different resources and access from different users.
Allocating operations to the right resources while ensuring a fair queueing is an important behavior, especially when you scale your workload.

Polyaxon provides several interfaces designed to achieve fairness when a limited resource is shared,
for example, to prevent a hyperparameter tuning with large search space or parallel executions from consuming more cluster resources than other workflows and operations.

## Features

Polyaxon provides several tools to:
 * Limit workflows from running a large number of concurrent operations.
 * Prioritize some important operations.
 * Route operations that require special resources to the right node(s), namespace, or cluster.
 * Split your workload over several nodes and clusters.

## Concepts

There are several distinct features involved in the scheduling strategies:

 * [Node scheduling](/docs/core/scheduling-strategies/node-scheduling/): A feature that leverages the Kubernetes API to select nodes for running your operations.
 * [Resources scheduling](/docs/core/scheduling-strategies/resources-scheduling/): A feature that leverages the Kubernetes API to enable GPU/TPU, or other special resources for your operations.
 * [Queue priority](/docs/core/scheduling-strategies/queue-routing/#priority): A feature to prioritize operations on a queue.
 * [Queue concurrency](/docs/core/scheduling-strategies/queue-routing/#concurrency): A feature to throttle the number of operations on a queue based on parallelism.
 * Queue Resources (**Roadmap**): A feature to throttle the number of operations on a queue based on resources (CPU/Memory/GPU/...).
 * [Queue agent](/docs/core/scheduling-strategies/queue-routing/#agent): A feature to route operations on a queue to a namespace or cluster.
 * [Concurrency management](/docs/core/scheduling-strategies/concurrency-management): A feature to limit the number of operations queued.
 * [Scheduling presets](/docs/core/scheduling-strategies/presets/): A feature for injecting certain information into operations at compilation time to preset configuration
   for node scheduling, queue routing, resources requirements and definition, connections, and access level control.
 * [Resume & Restart](/docs/core/scheduling-strategies/resume-restart/): Scheduling operation by resuming, restarting, and copying previous operation runs.
 * [Conditional scheduling](/docs/core/scheduling-strategies/conditional-scheduling/): A feature to start operation on nodes or queues based on inputs data or to completely skip scheduling the operation.
 * [Manual approval](/docs/core/scheduling-strategies/manual-approval/): A feature to pause and suspend operations and pipelines and wait for human approval to resume the work.
 * [Operation cache layer](/docs/core/scheduling-strategies/operations-caching/): A feature to reduce the cost and execution time by avoiding and skipping similar work.
 * [External scheduling](/docs/core/scheduling-strategies/external-scheduling/): A feature to schedule and submit operations from external systems.
