---
title: "Polyaxon Jobs Query Syntax"
sub_link: "polyaxon-query-syntax/jobs"
meta_title: "Polyaxon Jobs Query Syntax Specification - Polyaxon References"
meta_description: "Polyaxon Jobs Query Syntax Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - query
    - syntax
    - search
    - job
    - tracking
    - insights
sidebar: "polyaxon-query-syntax"
---

# Searching Jobs

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
`build.id`                    | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`project.*` (e.g. project.id) | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`commit`                      | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`name`                        | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`status`                      | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)
`tags`                        | [value condition](/references/polyaxon-query-syntax/#query-with-value-condition)


## Sort

field:

 * `created_at`
 * `updated_at`
 * `started_at`
 * `finished_at`
