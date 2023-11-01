---
title: "Schedules"
sub_link: "schedules"
meta_title: "Polyaxon Schedules - Polyaxon Automation Reference"
meta_description: "To be able to trigger a component repeatedly, a pipeline must define a schedule."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - polyflow
  - pipelines
  - dags
  - schedules
sidebar: "automation"
---

## Overview

Components are by default triggered one time when a user creates an operation,
or as many times as the users trigger new operations.
Polyaxon monitors all operations and all DAGs, and triggers ops whose dependencies have been met.

To be able to trigger components repeatedly, the operation must define a schedule.
Polyaxon provides several scheduling interfaces to automate the process of creating runs.

 * [Cron schedules](/docs/automation/schedules/cron/)
 * [Interval schedules](/docs/automation/schedules/interval/)
 * [Exact time schedules](/docs/automation/schedules/datetime/)


## Cache

When running operations on schedule, Polyaxon will automatically check if an operation has changed and will trigger a cache hit if no changes were detected.
If you intend to run the same operation (same manifest and same inputs/outputs/params) without changes, we suggest that you disable the cache:

```yaml
version: 1.1
kind: operation
schedule:
  kind: ...
  ...
cache:
  disable: true
...
```

Alternatively, to keep using the cache while triggering a schedule tick, you can use the `schedule_at` variable and pass it as a param, if your component is expecting it as an input or as context only param if it's not expected:


```yaml
version: 1.1
kind: operation
schedule:
  kind: ...
params:
  schedule_at:
    value: '{{ globals.schedule_at }}'
    contextOnly: true
...
```

By providing the `schedule_at` variable, you can leverage the cache mechanism and trigger a unique operation based on the manifest configuration.
