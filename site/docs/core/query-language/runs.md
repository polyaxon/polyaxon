---
title: "Runs Query Syntax"
sub_link: "query-language/runs"
meta_title: "Polyaxon Experiments Query Syntax Specification - Polyaxon References"
meta_description: "Polyaxon Experiments Query Syntax Specification."
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

# Searching Runs

## Aliases

Several fields accept aliases:

 * id: uid, uuid
 * inputs: in, params
 * outputs: out, metrics

> N.B. the difference between `outputs` and `metrics`: outputs use value condition, and metrics use comparison condition.

## Query

field                           | condition
--------------------------------|------------------
`id`                            | [string condition](/docs/core/query-language/#query-with-value-condition)
`name`                          | [string condition](/docs/core/query-language/#query-with-string-condition)
`description`                   | [string condition](/docs/core/query-language/#query-with-string-condition)
`created_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`updated_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`started_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`finished_at`                   | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`user`                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`project.*` (e.g. project.name) | [value condition](/docs/core/query-language/#query-with-value-condition)
`status`                        | [value condition](/docs/core/query-language/#query-with-value-condition)
`tags`                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`inputs.*`                      | [value condition](/docs/core/query-language/#query-with-value-condition)
`outputs.*`                     | [value condition](/docs/core/query-language/#query-with-value-condition)
`metrics.*`                     | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`duration`                      | [comparison condition](/docs/core/query-language/#query-with-comparison-condition)
`commit`                        | [value condition](/docs/core/query-language/#query-with-value-condition)
`agent`                         | [value condition](/docs/core/query-language/#query-with-value-condition)
`queue`                         | [value condition](/docs/core/query-language/#query-with-value-condition)
`meta_flags`                    | [bool condition](/docs/core/query-language/#query-with-bool-condition)
`live_state`                    | [value condition](/docs/core/query-language/#query-with-value-condition)


## Sort

field:

 * `created_at`
 * `updated_at`
 * `started_at`
 * `finished_at`
 * `inputs.*`
 * `outputs.*`
 * `metrics.*`
