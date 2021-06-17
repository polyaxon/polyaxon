---
title: "Queues"
sub_link: "scheduling-strategies/queues"
meta_title: "Queue routing in Polyaxon - Scheduling strategies"
meta_description: "Polyaxon provides a queue abstraction to prioritize operations on a queue,
to throttle the number of operations on a queue,
to route operations on a queue to a namespace or cluster,
to limit the number of operations queued from a single workflow or nested workflows."
tags:
  - configuration
  - polyaxon
  - kubernetes
  - environment
  - scheduling
  - orchestration
  - nodes
sidebar: "core"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Polyaxon provides a queue abstraction to:
  * Prioritize operations on a queue.
  * Throttle the number of operations on a queue.
  * Setting quota and restrictions on resources (CPU/Memory/GPU/TPU/Custom/...) or on cost.
  * Route operations on a queue to a namespace or cluster.
  * Limit the number of operations queued from a single workflow or nested workflows.

## Concepts

### Agents

Polyaxon can manage multiple agents, each agent can manage a namespace or a cluster. These namespaces do not have to be on the same cluster,
which allows a single Polyaxon control plane to use multiple Kubernetes clusters as worker nodes for scheduling jobs.

Each agent can manage multiple queues to prioritize which operations the agent should schedule first.

> To deploy an agent please check the [agent setup page](/docs/setup/agent/)

> To manage agents please check the [management section](/docs/management/organizations/agents/)

### Queues

A queue is a concept that Polyaxon uses to prepare fully compiled and resolved operations before routing them to the namespace/cluster where they should be running on.

Every queue in Polyaxon can define a priority and a concurrency. By default, queues are created with the maximum concurrency limit and the highest priority level.
In that case, if a queue is created with the default configuration it will be used only for routing purposes.

 * Concurrency: By default, each queue is created with the maximum concurrency limit, unless the user sets a concurrency limit [-1, ...].

 * Priority: By default, each queue is created with the highest priority, unless the user sets a priority level [-1, ...].
 
 * Quota: By default, each queues is created withtout any quota and allows any amount of resources.

> To manage queues please check the [management section](/docs/management/organizations/queues/)

## Queueing

When a user runs an independent operation, Polyaxon will automatically start compiling and resolving that operation and will put it on the queue defined in the operation,
if no queue is defined in the operation, the default queue assigned to the project will be used.

> To define a queue on the [component](/docs/core/specification/component/#queue),
> on the [operation](/docs/core/specification/operation/#queue),
> using the [CLI's](/docs/core/cli/run/) `--queue` flag, or using the [client's create methods](/docs/core/python-library/run-client/#create)

If a user runs a workflow with concurrency defined, e.g. parallel executions, DAGs, hyperparameter optimization,
Polyaxon will use the right algorithm for generating any dynamic operations
(topological sorting for DAGs, mapping for parallel executions, and the correct hyperparameter tuning search algorithm for optimization)
to generate the operations and will only compile and resolve operations that have a fully defined upstream dependency and resolved conditions and triggers.
It will then start to queue operations on the requested queues up to the concurrency defined by the workflow.

Once the operations are queued, Polyaxon will follow the routing process defined in the next section to route and schedule operation on the right namespace/cluster.


## Routing

Polyaxon uses the priority, concurrency, and quota definitions on the queues to organize and schedule your operations.
The concurrency limits defined by the queues are summed and then the sum is divided up among the priority levels.
Polyaxon will dispatch and schedule operations based on the queue priority they belong to until each queue reaches the concurrency limit allowed or the resource/cost quota allowed.

Each namespace (same cluster or different cluster) will receive operations from the queues they are subscribed to via the agent managing the namespace.

## Node scheduling

Once the operation is on the namespace/cluster, the agent will execute final resolutions required to start the operation,
if the operation defines node scheduling it will be further scheduled on the requested node(s).

## Global or per project queues

Managers and Admins of Polyaxon organizations and projects can set a default queue that gets applied to all runs under the organization or the project.

Setting the organization's default queue:

![default-org-preset](../../../../content/images/dashboard/queues/default-org-queue.png)

Setting a project's default queue:

![default-project-preset](../../../../content/images/dashboard/queues/default-project-queue.png) 

Restricting queues accessible by a project:

![default-project-preset](../../../../content/images/dashboard/queues/queues-restrictions.png)

## Observability

Using the cli command:

```bash
polyaxon ops statuses -w
```

Or the statuses page:

![Runs statuses](../../../../content/images/dashboard/runs/statuses.png)

You get a full overview of the timeline of each stage, and if during the lifecycle of an operation an error
occurs or an exception is raised,
a red status will be saved with a condition containing information about how to debug the cause of the error.
