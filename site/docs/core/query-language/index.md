---
title: "Polyaxon Query Language"
sub_link: "query-language"
meta_title: "Polyaxon Query Language Specification - Polyaxon References"
meta_description: "Polyaxon Query Language Specification."
visibility: public
status: published
is_index: true
tags:
  - api
  - reference
  - polyaxon
  - query
  - syntax
  - search
sidebar: "core"
---

# Understanding the query syntax

When searching experiments, jobs, projects, or any entity on Polyaxon,
you can construct queries that match specific numbers and words.
You can as well change the sorting mechanism of the results.

## Sort

To update the sort of an API, CLI command, or on the dashboard, you just need to provide one or
multiple fields, comma separated, that you wish to use for the sorting, either ascending or descending with the `-` modifier.

Examples:

 * Sort by creation date: `sort="created_at"`
 * Sort by creation date descending and start date ascending: `sort="-created_at, started_at"`
 * Sort by finished date and loss: `finished_at, metrics.loss`

## Query with scalar condition

This is useful to compare to scalar values, e.g. metrics, number values like concurrency ...
you can search for values that are equal, not equal, greater than,
greater than or equal to, less than, and less than or equal to another value.

operator         | example
-----------------|------------------
`x is None`      | `metrics.loss: nil` will match all entities that have a null/none metric loss
`x is not None`  | `metrics.loss: ~nil` will match all entities that have a non null metric loss
`x = n`          | `metrics.loss: 0.1` will match all entities that have a metric loss equal to 0.1
`x != n`         | `metrics.loss: ~0.1` will match all entities that have a metric loss not equal to 0.1
`x > n`          | `metrics.loss: >0.1` or with negation `metrics.loss: ~<=0.1` will match all entities that have a metric loss greater than 0.1
`x >= n`         | `metrics.loss: >=0.1` or with negation `metrics.loss: ~<0.1` will match all entities that have a metric loss greater than or equal 0.1
`x < n`          | `metrics.loss: <0.1` or with negation `metrics.loss: ~>=0.1` will match all entities that have a metric loss less than 0.1
`x <= n`         | `metrics.loss: <=0.1` or with negation `metrics.loss: ~>0.1` will match all entities that have a metric loss less than or equal than 0.1

To search for a range or outside a range you can combine two operators:

operator                                 | example
-----------------------------------------|------------------
`n <[=] x <[=] m` where n < m            | `metrics.loss:>0.1, metrics.loss:<0.4` will match all entities that have a metric strictly between 0.1 and 0.4
`x <[=] n` and `x >[=] m`  where n < m   | `metrics.loss:<=0.1, metrics.loss:>=0.4` will match all entities that have a metric outside the range 0.1 and 0.4

You can of course use any combination of the operators with negation modifier.

## Query with cpu condition

Similar to the query with scalar condition, and in addition to the int/float values, it accepts any valid Kubernetes CPU value e.g. 1, 100, 0.75, 750m, ...  

## Query with memory condition

Similar to the query with scalar condition, and in addition to the int/float values, it accepts any valid Kubernetes memory value e.g. 128974848, 129e6, 129M, 123Mi, 4Gi, ...

## Query with value condition

This is useful to compare categorical values, e.g. statuses, search algorithm, ids, commit hash, ...
you can search for values that are equal, not equal, in a set of values, or not in a set of values.


operator               | example
-----------------------|------------------
`x is None`            | `name: nil` will match all entities that have a null/none name
`x is not None`        | `name: ~nil` will match all entities that have a non null name
`x = y`                | `status: running` will match all entities that have the status running
`x != y`               | `status: ~running` will match all entities that have the status not running
`x in {a, b, c}`       | <code>status: started &#124; building &#124; running</code> will match all entities that have the status in one of the values started, building, or running
`x not in {a, b, c}`   | <code>status: ~started &#124; building &#124; running</code> will match all entities that have the status not in one of the values started, building, or running


## Query with bool condition

This is useful to compare boolean values, e.g. flags.
you can search for values that are equal, not equal to a value that can be converted to a boolean, e.g. 1/true/t/True and 0/false/f/False.


operator               | example
-----------------------|------------------
`x = 1`                | `flag: true` will match all entities that have the status running
`x != 0`               | `flag: ~false` will match all entities that have the status not running


## Query with datetime condition

This is useful to compare date and datetime values, e.g. created_at, updated_at, started_at, finished_at, ...
you can search for values that are equal, not equal, greater than, greater than or equal to,
less than, less than or equal to, or in date range.

operator                                                                  | example
--------------------------------------------------------------------------|------------------
`x = YYYY-MM-DD`, `x = YYYY-MM-DD HH:MM`, `x = YYYY-MM-DD HH:MM:SS`       | `created_at: 2018-10-01` will match all entities that have were created at 2018-10-01 (you can be more precise by providing hours and minutes)
`x != YYYY-MM-DD`, `x != YYYY-MM-DD HH:MM`, `x != YYYY-MM-DD HH:MM:SS`    | `created_at: ~2018-10-01` will match all entities that have were not created at 2018-10-01 (you can be more precise by providing hours and minutes)
`x > YYYY-MM-DD`, `x > YYYY-MM-DD HH:MM`, `x > YYYY-MM-DD HH:MM:SS`       | `created_at: >2018-10-01` will match all entities that have were created at strictly after 2018-10-01 (you can be more precise by providing hours and minutes, and you can negate with `~`)
`x >= YYYY-MM-DD`, `x >= YYYY-MM-DD HH:MM`, `x >= YYYY-MM-DD HH:MM:SS`    | `created_at: >=2018-10-01` will match all entities that have were created at starting from 2018-10-01 (you can be more precise by providing hours and minutes, and you can negate with `~`)
`x < YYYY-MM-DD`, `x < YYYY-MM-DD HH:MM`, `x < YYYY-MM-DD HH:MM:SS`       | `created_at: <2018-10-01` will match all entities that have were created at strictly before 2018-10-01 (you can be more precise by providing hours and minutes, and you can negate with `~`)
`x <= YYYY-MM-DD`, `x <= YYYY-MM-DD HH:MM`, `x <= YYYY-MM-DD HH:MM:SS`    | `created_at: <=2018-10-01` will match all entities that have were not created until 2018-10-01 (you can be more precise by providing hours and minutes, and you can negate with `~`)

To search for ranges you have 2 ways to do that either by combining queries as it was seen in the comparison, or by using the `..` operator

operator                     | example
-----------------------------|------------------
`YYYY-MM-DD .. YYYY-MM-DD`   | `created_at: 2018-10-01 .. 2019-10-01` will match all entities that were created between 2018-10-01 and 2019-10-01 (you can be more precise by providing hours and minutes)
`~YYYY-MM-DD .. YYYY-MM-DD`  | `created_at: ~2018-10-01 .. 2019-10-01` will match all entities that were created before 2018-10-01 and after 2019-10-01 (you can be more precise by providing hours and minutes)

## Query with string condition

This is useful to compare string values, e.g. name and description.
you can search for values that are equal, not equal, in a set of values, or not in a set of values, start with, end with, start with and end with.


operator                    | example
----------------------------|------------------
`x = y`                     | `status: running` will match all entities that have the status running
`x != y`                    | `status: ~running` will match all entities that have the status not running
`x in {a, b, c}`            | <code>status: started &#124; building &#124; running</code> will match all entities that have the status in one of the values started, building, or running
`x not in {a, b, c}`        | <code>status: ~started &#124; building &#124; running</code> will match all entities that have the status not in one of the values started, building, or running
`x ends with foo`           | `x: %foo` will match all entities that have the value ending with foo
`x starts with foo`         | `x: foo%` will match all entities that have the value starting with foo
`x starts/ends with foo`    | `x: %foo%` will match all entities that have the value starting/ending with foo


## Query with the negation modifier

You can negate any condition by prefixing the query with `~`, e.g `x:~2` is the equivalent of saying is different than 2.

## Query for null/none values

You can check for null or non null values by using the special operator `nil`, e.g `x:nil` is the equivalent of saying x should be null/none,
the nil operator can be used with negation as well, e.g. `x:~nil`.

## Query by combining multiple conditions

Every time you put a comma `,` Polyaxon will filter further by the condition that comes after the comma.

## Entities

Polyaxon supports searching all entities using this syntax, most common entities are:

 * [Runs](/docs/core/query-language/runs/)
 * [Projects](/docs/core/query-language/projects/)


## Saved searches

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

You can save searches to access and apply filters to several projects and runs, saved searches can be accessed by other team members to avoid reconstructing similar filters.
Please check [management - searches](/docs/management/organizations/searches/).
