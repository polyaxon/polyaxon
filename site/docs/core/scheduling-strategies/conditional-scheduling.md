---
title: "Conditional Scheduling"
sub_link: "scheduling-strategies/conditional-scheduling"
meta_title: "How to conditionally schedule operations in Polyaxon - scheduling strategies"
meta_description: "A feature to start operations on nodes or queues based on inputs data or to completely skip scheduling."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

Polyaxon resolves a [context](/docs/core/context/) based on the inputs provided by the users, such information can be used to parametrize and template section responsible for scheduling and queueing.

Polyaxon will substitute all variable references in the environment, presets, and queue section after resolving the full context.

## Templating the presets section

Conditional list of presets based on the value of some parameter value:

```yaml
presets: {{ [preset1] if input_param == value_condition else list2 }}
```

Parametrized list of presets:

```yaml
presets: {{ input_param | list }}
```

## Templating the queue section

Conditional queue based on the value of some parameter value:

```yaml
queue: {{ AGENT_X1/QUEUE_Y1 if input_param == value_condition else AGENT_2/QUEUE_2 }}
```

Parametrized agent and/or queue values:

```yaml
queue: {{ agent_param }}/{{ queue_param }}
```

Parametrized agent and queue:

```yaml
queue: {{ fqn_queue_param }}
```


## Templating the environment section

Example with `nodeSelector`:

```yaml
environment:
 nodeSelector:
    "{{ node_param }}": "node-{{ node_label }}"
```

Conditional node name:

```yaml
environment:
 nodeName: "{{ node_name1 if input_param == value_condition else node_name2 }}"
```

Parametrized node name:

```yaml
environment:
 nodeName: "{{ node_param }}"
```

Similar logic can be used for other `environment.*` sections.

## Conditional scheduling

In order to skip an operation, you can use the `conditions` key:

```yaml
conditions: "{{ input_param == value_condition }}"
```

Or

```yaml
conditions: "input_param == value_condition"
```

Polyaxon always assumes that conditions are parametrized and need to be resolved.

If the condition is `false` the operation will be skipped.

> **Note**: Although it's possible to use conditions in an independent operation,
> it generally makes more sense when it's running in the context of a pipeline (DAG, Matrix, or Schedule), when an operation is used as a hook, or when an operation is subscribing to events.

