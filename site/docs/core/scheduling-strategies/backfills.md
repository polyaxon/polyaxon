---
title: "Running backfills"
sub_link: "scheduling-strategies/backfills"
meta_title: "How to running backfills - scheduling strategies"
meta_description: "A feature to execute an operation over a date range or datetime rage with or without concurrency."
visibility: public
status: published
tags:
  - concepts
  - tutorials
sidebar: "core"
---

## Overview

Users can leverage the `matrix` section with the grid search algorithm to execute backfills.
Polyaxon provides a [daterange](/docs/automation/optimization-engine/params/#v1hpdaterange) and a [datetimerange](/docs/automation/optimization-engine/params/#v1hpdatetimerange)
generators that can be used to specify interval to use for running the backfill. Users can also specify if they need to execute the backfill sequentially by setting
the concurrency to `1`.

## IO of a backfill operation

In order to correctly execute a backfill, users should only create a matrix with a single search param. The component can expect several inputs/outputs,
but it should expect one of the inputs/outputs to be of type `date` or `datetime`.

### Backfill Component

Hourly backfill example:

```yaml
version: 1.1
kind: component
name: hourly-backfill
inputs:
- {name: dt, type: datetime}
- {name: dummy_input1, type: str}
- {name: dummy_input2, type: int}
run:
  kind: job
  container:
    image: DOCKER_IMAGE
    command: ["execute", "backfill"]
    args: ["--hour={{ dt }}"]
```

Daily backfill example:

```yaml
version: 1.1
kind: component
name: daily-backfill
inputs:
- {name: dt, type: date}
- {name: dummy_input1, type: str}
- {name: dummy_input2, type: int}
run:
  kind: job
  container:
    image: DOCKER_IMAGE
    command: ["execute", "backfill"]
    args: ["--day={{ dt }}"]
```

### Backfill Operations

Hourly backfill example:

```yaml
version: 1.1
kind: operations
params:
  dummy_input1: {value: "test"}
  dummy_input2: {value: 10}
matrix:
  kind: grid
  concurrency: 1
  params:
    dt:
      kind: datetimerange
      value: ["2021-05-01 10:00", "2021-05-01 16:00", 3600]
```

Daily backfill example:

```yaml
version: 1.1
kind: operations
params:
  dummy_input1: {value: "test"}
  dummy_input2: {value: 10}
matrix:
  kind: grid
  concurrency: 1
  params:
    dt:
      kind: daterange
      value: ["2021-05-01", "2021-05-08", 1]
```

## Alternative

Users can manually create a mapping to generate the combination to iterate over or can use the Python client to loop over the range manually and submit jobs.
The main difference between using the matrix for creating a backfill and using the Python client manually is the visibility of the backfill progress and the concurrency control.

By using the matrix, users can control if the operations must execute sequentially or based on a specific concurrency value, they can also quickly view all the operations
grouped under the matrix operations, and can leverage the timeline view, the analytics view, and the pipeline progress view to quickly see which operations failed.
