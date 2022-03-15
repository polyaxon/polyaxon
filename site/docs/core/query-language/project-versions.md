---
title: "Project Versions (component/model/artifact) Query Syntax"
sub_link: "query-language/project-versions"
meta_title: "Polyaxon Query Syntax Specification for Project Versions - Polyaxon References"
meta_description: "Polyaxon Query Syntax Specification for Project Versions."
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

field                           | condition
--------------------------------|------------------
`id` or `uuid`                  | [string condition](/docs/core/query-language/#query-with-value-condition)
`name`                          | [string condition](/docs/core/query-language/#query-with-string-condition)
`description`                   | [string condition](/docs/core/query-language/#query-with-string-condition)
`created_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`updated_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`tags`                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`kind`                          | [value condition](/docs/core/query-language/#query-with-value-condition)
`stage`                         | [value condition](/docs/core/query-language/#query-with-value-condition)
`state`                         | [value condition](/docs/core/query-language/#query-with-value-condition)


## Sort

field:

 * `created_at`
 * `updated_at`
 * `kind`
 * `stage`
 * `state`

