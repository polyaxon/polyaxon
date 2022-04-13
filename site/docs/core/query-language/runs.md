---
title: "Runs Query Syntax"
sub_link: "query-language/runs"
meta_title: "Polyaxon Query Syntax Specification for Runs - Polyaxon References"
meta_description: "Polyaxon Runs/Experiments Query Syntax Specification for Runs."
visibility: public
status: published
tags:
  - api
  - reference
  - polyaxon
  - query
  - syntax
  - search
  - experiment
  - tracking
  - insights
sidebar: "core"
---

## Aliases

Several fields accept aliases:

 * id: uid, uuid
 * inputs: in, params
 * outputs: out, metrics

> **N.B.** the difference between `outputs` and `metrics`: `outputs.*` use [value condition](/docs/core/query-language/#query-with-value-condition) and `metrics.*` use [comparison condition](/docs/core/query-language/#query-with-comparison-condition).

## Query

field                                                                      | condition
---------------------------------------------------------------------------|------------------
`id` or `uuid`                                                             | [string condition](/docs/core/query-language/#query-with-value-condition)
`name`                                                                     | [string condition](/docs/core/query-language/#query-with-string-condition)
`description`                                                              | [string condition](/docs/core/query-language/#query-with-string-condition)
`created_at`                                                               | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`updated_at`                                                               | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`started_at`                                                               | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`finished_at`                                                              | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`user`                                                                     | [value condition](/docs/core/query-language/#query-with-value-condition)
`project.*` (e.g. project.name)                                            | [value condition](/docs/core/query-language/#query-with-value-condition)
`status`                                                                   | [value condition](/docs/core/query-language/#query-with-value-condition)
`tags`                                                                     | [value condition](/docs/core/query-language/#query-with-value-condition)
`inputs.*`                                                                 | [value condition](/docs/core/query-language/#query-with-value-condition)
`outputs.*`                                                                | [value condition](/docs/core/query-language/#query-with-value-condition)
`metrics.*`                                                                | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`duration`                                                                 | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`wait_time`                                                                | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`commit`                                                                   | [value condition](/docs/core/query-language/#query-with-value-condition)
`agent`                                                                    | [value condition](/docs/core/query-language/#query-with-value-condition)
`queue`                                                                    | [value condition](/docs/core/query-language/#query-with-value-condition)
`artifacts_store`                                                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`kind`                                                                     | [value condition](/docs/core/query-language/#query-with-value-condition)
`runtime`                                                                  | [value condition](/docs/core/query-language/#query-with-value-condition)
`namespace`                                                                | [value condition](/docs/core/query-language/#query-with-value-condition)
`meta_info.*`                                                              | [value condition](/docs/core/query-language/#query-with-value-condition)
`meta_values.*` (e.g. meta_values.iteration)                               | [value condition](/docs/core/query-language/#query-with-value-condition)
`meta_flags.*` (e.g. meta_flags.has_events or meta_flags.has_tensorboard)  | [bool condition](/docs/core/query-language/#query-with-bool-condition)
`live_state`                                                               | [value condition](/docs/core/query-language/#query-with-value-condition)
`pipeline` (equivalent to pipeline.uuid)                                   | [value condition](/docs/core/query-language/#query-with-value-condition)
`pipeline.*` (e.g. pipeline.kind or pipeline.runtime)                      | [value condition](/docs/core/query-language/#query-with-value-condition)
`controller` (equivalent to controller.uuid)                               | [value condition](/docs/core/query-language/#query-with-value-condition)
`controller.*` (e.g. controller.kind or controller.runtime)                | [value condition](/docs/core/query-language/#query-with-value-condition)
`original` (equivalent to original.uuid)                                   | [value condition](/docs/core/query-language/#query-with-value-condition)
`original.*` (e.g. original.name)                                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`cloning_kind` (cloud be one of the valid cloning kind, e.g. restart)      | [value condition](/docs/core/query-language/#query-with-value-condition)
`artifacts` (equivalent to artifacts.state)                                | [value condition](/docs/core/query-language/#query-with-value-condition)
`artifacts.*` (e.g. artifacts.name, artifacts.path or artifacts.kind)      | [value condition](/docs/core/query-language/#query-with-value-condition)
`connections` (equivalent to connections.name)                             | [value condition](/docs/core/query-language/#query-with-value-condition)
`connections.*` (e.g. connections.name or connections.kind)                | [value condition](/docs/core/query-language/#query-with-value-condition)
`upstream` (equivalent to upstream.uuid)                                   | [value condition](/docs/core/query-language/#query-with-value-condition)
`upstream.*` (e.g. upstream.name)                                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`downstream` (equivalent to downstream.uuid)                               | [value condition](/docs/core/query-language/#query-with-value-condition)
`downstream.*` (e.g. downstream.name)                                      | [value condition](/docs/core/query-language/#query-with-value-condition)
`component_state`                                                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`pending`                                                                  | [value condition](/docs/core/query-language/#query-with-value-condition)
`cost`                                                                     | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`cpu`                                                                      | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`memory`                                                                   | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`gpu`                                                                      | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`custom`                                                                   | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)

## Sort

field:

 * `created_at`
 * `updated_at`
 * `started_at`
 * `finished_at`
 * `user`
 * `duration`
 * `wait_time`
 * `kind`
 * `status`
 * `component_state`
 * `runtime`
 * `inputs.*`
 * `outputs.*`
 * `metrics.*`
 * `agent`
 * `queue`
 * `artifacts_store`
 * `cost`    
 * `cpu`      
 * `memory`   
 * `gpu`   
 * `custom`
