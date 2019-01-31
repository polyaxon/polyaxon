---
title: "Polyaxon Experiment Groups Query Syntax"
sub_link: "polyaxon-query-syntax/experiment-groups"
meta_title: "Polyaxon Experiment Groups Query Syntax Specification - Polyaxon References"
meta_description: "Polyaxon Experiment Groups Query Syntax Specification."
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
    - groups
    - optimization
    - tracking
    - insights
sidebar: "polyaxon-query-syntax"
---

# Searching Experiment Groups

## Query

field                         | condition
------------------------------|------------------
`id`                          | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`created_at`                  | [datetime condition](/references/polyaxon-query-syntax/#query-with-datetime-condition)
`updated_at`                  | [datetime condition](/references/polyaxon-query-syntax/#query-with-datetime-condition)
`started_at`                  | [datetime condition](/references/polyaxon-query-syntax/#query-with-datetime-condition)
`finished_at`                 | [datetime condition](/references/polyaxon-query-syntax/#query-with-datetime-condition)
`user.id`                     | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`user.username`               | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`project.*` (e.g. project.id) | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`name`                        | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`status`                      | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`tags`                        | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`search_algorithm`            | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`concurrency`                 | [comparison condition](/references/polyaxon-query-syntax/#query-with-comparison-condition)


## Sort

field:

 * `created_at`
 * `updated_at`
 * `started_at`
 * `finished_at`
