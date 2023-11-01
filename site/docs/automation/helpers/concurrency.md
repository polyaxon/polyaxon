---
title: "Workflow Concurrency Management"
sub_link: "helpers/concurrency"
meta_title: "Concurrency - Polyaxon Specification"
meta_description: "Polyaxon manages concurrency on pipeline level and on queue level."
visibility: public
status: published
tags:
  - specification
  - api
  - polyaxon
  - yaml
  - json
  - python
sidebar: "automation"
---

## Overview

Several automation tools provided by Polyaxon can run multiple operations in parallel,
e.g. DAGs, parallel executions, mapping, hyperparameter tuning, ...

There are situations in which users want to actively prevent too many operations
from running in parallel.

## Management

Polyaxon can manage concurrency on any workflow that runs more than one operation.
There are several ways to manage concurrency:

 * Directly on the workflow using the `concurrency` field.
 * Globally using a [queue](/docs/core/scheduling-strategies/queues/).
 * Both.

## Control flow

When a workflow defines a `concurrency` field, Polyaxon will only queue a maximum of operations equal to the concurrency.
If no concurrency is set on a workflow, Polyaxon will queue any operations that it's full compiled and resolved in the workflow.

When an operation is queued, using the default queue or following the `queue` field if defined on the operation,
the operation will not immediately be scheduled to be executed, there's a process to check the priority of each queue,
and it only schedules the number of operations based on the queue's concurrency setting.

This how Polyaxon checks when to queue and execute an operation:

 * Check if the workflow directly managing the operation can queue more operations based on the concurrency field
    (i.e. max concurrency, if no concurrency is set then it's considered unlimited)
 * Check if this workflow is running in the context of a meta workflow, i.e nested in a controller workflow, check the concurrency of that workflow.
 * Queue the operation on the requested queue, if no queue is set then use the default queue of the project.
 * Check if the queue can schedule more operations based on their priority and concurrency definitions.
 * Schedule and run the operation.

Please check this guide for more details about [scheduling with queues](/docs/core/scheduling-strategies/queues/)

## Nested flows

Since it's possible to nest workflows, e.g. a dag running in parallel, or dag inside a dag.

Polyaxon keeps up to 2 main workflows for queueing operations:
 * Direct Pipeline: the workflow directly managing an operation.
 * Controller Pipeline: a meta workflow referencing the parent pipeline.

Even if the concurrency of a workflow allows to queue an operation,
if the controller workflow has exhausted its maximum concurrency,
the operation from the nested workflow will not be queued and will have to wait until
the controller workflow can queue more operations.
