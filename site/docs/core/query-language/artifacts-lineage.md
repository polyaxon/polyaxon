---
title: "Artifacts Lineage Query Syntax"
sub_link: "query-language/artifacts-lineage"
meta_title: "Polyaxon Query Syntax Specification for Artifacts Lineage - Polyaxon References"
meta_description: "Polyaxon Query Syntax Specification for Artifacts Lineage."
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

## Query

field                                                   | condition
--------------------------------------------------------|------------------
`id` or `uuid`                                          | [string condition](/docs/core/query-language/#query-with-value-condition)
`name`                                                  | [string condition](/docs/core/query-language/#query-with-string-condition)
`kind`                                                  | [value condition](/docs/core/query-language/#query-with-value-condition)
`state`                                                 | [value condition](/docs/core/query-language/#query-with-value-condition)
`path`                                                  | [value condition](/docs/core/query-language/#query-with-value-condition)
`is_input`                                              | [bool condition](/docs/core/query-language/#query-with-bool-condition)
`run` (equivalent to run.uuid)                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`run.*` (e.g. run.name)                                 | [value condition](/docs/core/query-language/#query-with-value-condition)

## Sort

field:

 * `name`
 * `kind`
 * `path`
 * `is_input`

