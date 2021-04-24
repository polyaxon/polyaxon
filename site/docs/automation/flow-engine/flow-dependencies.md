---
title: "Flow Dependencies"
sub_link: "flow-engine/flow-dependencies"
meta_title: "Flow Engine Dependencies Between Operations - Polyaxon References"
meta_description: "Managing dependencies between operation in a DAG."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - automation
  - workflow
  - pipelines
sidebar: "automation"
---

## Overview

Dags expose several ways to define dependencies between operations:
 * Using the `dependencies` field.
 * Using a parameter reference.
 * Using an event reference.

In addition to the `dependencies` definition, users can add `trigger` and `conditions`
to perform extra checks on the state of those dependencies.

## Dependencies

The `dependencies` is the simplest way to specify dependencies between operations in a DAG, 
it's explicit and requires that you specify a list of other tasks the current task depends on.

If an operation must wait for other operations and does not expect
any parameters from those operations, you can define the dependency manually:

```yaml
run:
  kind: dag
  operations:
    - name: job1
      hubRef: component1:latest
      params:
        ...
    - name: job2
      hubRef: component1:2.1
      params:
        ...
    - name: job3
      urlRef: https://some_url.com
      dependencies: [job1, job2]
```

`job1` and `job2` will run in parallel and job3 will wait for both jobs to finish.

> Note that when a dependency is defined via the `dependencies` you can only trigger the operation 
> when all upstream operation reach a final state following the `trigger` definition.

## Param dependencies

If an operation is expecting a parameter from the upstream operations,
we don't need to explicitly specify the dependencies `fields` for any operation that will have 
its dependency inferred from the params definition.

```yaml
run:
  kind: dag
  operations:
    - name: job1
      hubRef: component1:latest
      params:
        ...
    - name: job2
      hubRef: component1:2.1
      params:
        ...
    - name: job3
      urlRef: https://some_url.com
      dependencies: [job1]
      params:
        image:
          ref: ops.job2
          value: outputs.results
```

This is similar to the previous `dependencies` definition in the sense that
`job1` and `job2` will run in parallel and job3 will wait for both jobs to finish.

The dependency between `job2` and `job3` is inferred from the params definition.

## Trigger

In order to define a trigger condition or how to trigger `job3` based on the status `job1` and `job2`,
we can use the `trigger` field.
It determines if a task should run based on the statuses of the upstream tasks.

```yaml
- name: job3
  urlRef: https://some_url.com
  dependencies: [job1, job2]
  trigger: all_succeeded
```

Possible values: `all_succeeded`, `all_failed`, `all_done`, `one_succeeded`, `one_failed`, `one_done`

## skipOnUpstreamSkip

if `True`, if any immediately upstream tasks are skipped,
this task will automatically be skipped as well, regardless of other conditions or trigger.
By default, this prevents tasks from attempting to use an incomplete context
that won't be populated from the upstream tasks that didn't run.
If `False`, the task's trigger will be used with any skipped operations considered successes.

```yaml
- name: job3
  urlRef: https://some_url.com
  dependencies: [job1, job2]
  trigger: all_succeeded
  skipOnUpstreamSkip: true
```

## Conditions

Conditions are an advanced tool for resolving dependencies between operations.
Conditions take advantage of information resolved in the context to decide if an operation
can be started, and they can be used to define branching strategies.


```yaml
- name: job3
  urlRef: https://some_url.com
  dependencies: [job1]
  params:
    image:
      ref: ops.job2
      value: outputs.results
  conditions: '{{ image == "some-value" }}'
  skipOnUpstreamSkip: true
```

In the example above, `job3` will only run if the param passed is equal to "some-value".

## Event dependencies

Users will find that defining dependencies between operations using the `dependencies` fields is limiting, 
because it does not allow the user to specify which state of the task to depend on.

For example, a task may only be relevant to run if the dependent task start `running`, `succeeded`, `failed`, ...

Event dependencies provide the level of granularity and the option to define what specific event(s) should trigger the operation.

Also, since events define references, the dependency is inferred automatically and does not need to be set manually.

```yaml
- name: job3
  hubRef: "component:version"
  events:
    - ref: ops.job2
     kinds: [run_status_running]
``` 

In this example `job3` will be scheduled as soon as `job2` starts running.

> **Note**: For more details, please check the [events section](/docs/automation/events/specification/)
