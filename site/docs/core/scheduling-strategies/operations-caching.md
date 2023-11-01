---
title: "Operations Caching"
sub_link: "scheduling-strategies/operations-caching"
meta_title: "How to leverage the cache layer - scheduling strategies"
meta_description: "A feature to skip and avoid repetitive work and execute faster workflows."
visibility: public
status: published
tags:
  - concepts
  - tutorials
sidebar: "core"
---

## Overview

Polyaxon's operation cache is a feature to reduce the cost and execution time by avoiding and skipping similar work.

Oftentimes, operations can perform expensive computations to produce some outputs.
In order to leverage those results, without rerunning the same operations, Polyaxon provides a state that users can use to check if a computation is already performed or not.

> Please check the [cache specification](/docs/automation/helpers/cache/) for more details.

## Cache validation

Polyaxon comes with a cache resolver and validator, that informs the compiler if an operation instance is a cache hit.
By default the cache resolver:
   * Will be disabled automatically for independent runs created via CLI/API/UI, unless the user actively set the disable to `False`.
   * Will be disabled automatically for restart/resume ops.
   * Will be enabled automatically for all ops triggered automatically inside a pipeline (matrix/dag).
   * Can be set and enabled/disabled via the cache section, in which case the default behavior is not triggered, and the user's choice is honored.

## How to leverage the cache layer

Let's take an example where two users are collaborating on the same project, and running several hyperparameter tuning jobs.
One recurring problem is that the optimization algorithms might create similar suggestions and overlapping search spaces.
Without using the cache layer, Polyaxon will submit both jobs to your cluster, and both jobs will consume an equal amount of resources and run for almost similar durations.

By using the cache layer, Polyaxon will avoid submitting jobs with the same state, and will only run the first instance. Every operation that has the same definition will be flagged as a cache hit.
As soon as the original operation is done, Polyaxon will propagate the results to all dependent runs.

## Caching and artifacts

At the moment and in order to use the cache, users have to define the configuration that needs to be used in the state calculation via the params, otherwise, all params are considered in the calculation
(please check [cache specification](/docs/automation/helpers/cache/) for more details).

If you need to include an artifact in the state calculation, you can report a lineage metadata about that artifact, for example, the path or a hash, and set that value as an input.

> **Note**: We intend to make it easy to tell Polyaxon if it should consider the artifacts lineage in the state calculation.

## Further reading

### IO cache heuristic

If an operation needs to run in the future based on a schedule, or when a user initiates a hyperparameter tuning pipeline,
Polyaxon will memoize all params that can be resolved immediately, to avoid recalculating those values, and will only calculate the values that are specific to each run that is part of the pipeline.

### Artifacts cache

If an operation needs to start from the last checkpoint of a previous run, Polyaxon provides two mechanisms to cache the previous artifacts:

 * [Resume operations](/docs/core/scheduling-strategies/resume-restart/#resuming-operation)
 * [Restart operations with copy mode](/docs/core/scheduling-strategies/resume-restart/#restarting-operation-with-copy-mode)
