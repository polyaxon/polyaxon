---
title: "Projects Query Syntax"
sub_link: "query-language/projects"
meta_title: "Polyaxon Query Syntax Specification for Projects - Polyaxon References"
meta_description: "Polyaxon Projects Query Syntax Specification for Projects."
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
`name`                          | [string condition](/docs/core/query-language/#query-with-string-condition)
`description`                   | [string condition](/docs/core/query-language/#query-with-string-condition)
`created_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`updated_at`                    | [datetime condition](/docs/core/query-language/#query-with-datetime-condition)
`owner`                         | [string condition](/docs/core/query-language/#query-with-string-condition)
`tags`                          | [value condition](/docs/core/query-language/#query-with-value-condition)


## Sort

field:

 * `created_at`
 * `updated_at`
 * `name`
 * `owner`

