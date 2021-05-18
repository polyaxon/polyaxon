---
title: "Performance-based Tensorboard"
sub_link: "tensorboard/performance-based-tensorboard"
meta_title: "Performance-based Tensorboard - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Starting Tensorboard based on query specification - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

> **Note**: This section of the tutorial can only run on Polyaxon EE and Polyaxon Cloud.

In the previous tutorial, we learned how to list and filter runs and how to compare them using a Tensorboard component that expects multiple run uuids.
In this tutorial we will automate the complete process of querying runs, sorting based on the loss metric, limiting the results to 5 records, and then starting the Tensorboard.

## Querying runs with a Join

Polyaxon provides an abstraction called `join`. A join in Polyaxon allows to perform a search based on the `query`, `sort`, `limit`, and `offset` specification, and allows to pass the result to a component.

Let's look at how we can perform the previous process using a single polyaxonfile:

```yaml
version: 1.1
kind: operation
name: compare-top-experiments
joins:
- query: "kind:job, metrics.loss:<0.3, status:succeeded"
  sort: "metrics.loss"
  limit: "5"
  params:
    uuids: {value: "globals.uuid"}
hubRef: tensorboard:multi-run
```

This polyaxonfile contains an operation that basically performs a search and only requests the `uuid` of each run in the result, it then exposes those `uuids` as a parameter that the component expects.

> **Note**: For more details please check the [join section](/docs/automation/joins/).

## Running the join operation

Running an operation with a join is similar to running any other operation:

```bash
polyaxon run -f joins/performance_based_tensorboard.yaml [-p PROJECT_NAME] 
```

## Running a Tensorboard Join from the UI 

You can run run this join directly from the UI, and Polyaxon will start a Tensorboard service to compare the experiments. 
