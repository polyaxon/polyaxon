# Understanding the query syntax

When searching experiments, jobs, builds, or experiment groups on Polyaxon,
you can construct queries that match specific numbers and words.
You can as well change sorting mechanism of the results.

## Sort

To update the sort of an API, CLI command, or on the dashboard, you just need to provide one or
multiple fields, comma separated, that you wish to use for the sorting, either ascending or descending with the `-` modifier.

Examples:

 * Sort by creation date: `sort="created_at"`
 * Sort by creation date descending and start date ascending: `sort="-created_at, started_at"`
 * Sort by finished date and loss: `finished_at, metric.loss`

## Query with scalar condition

This is useful to compare to scalar values, e.g. metrics, number values like concurrency ...
you can search for values that are equal, not equal, greater than,
greater than or equal to, less than, and less than or equal to another value.

operator     | example
-------------|------------------
`x = n`      | `metric.loss: 0.1` will match all entities that have a metric loss equal to 0.1
`x != n`     | `metric.loss: ~0.1` will match all entities that have a metric loss not equal to 0.1
`x > n`      | `metric.loss: >0.1` or with negation `metric.loss: ~<=0.1` will match all entities that have a metric loss greater than 0.1
`x >= n`     | `metric.loss: >=0.1` or with negation `metric.loss: ~<0.1` will match all entities that have a metric loss greater than or equal 0.1
`x < n`      | `metric.loss: <0.1` or with negation `metric.loss: ~>=0.1` will match all entities that have a metric loss less than 0.1
`x <= n`     | `metric.loss: <=0.1` or with negation `metric.loss: ~>0.1` will match all entities that have a metric loss less than or equal than 0.1

To search for a range or outside a range you can combine two operators:

operator                                 | example
-----------------------------------------|------------------
`n <[=] x <[=] m` where n < m            | `metric.loss:>0.1, metric.loss:<0.4` will match all entities that have a metric strictly between 0.1 and 0.4
`x <[=] n` and `x >[=] m`  where n < m   | `metric.loss:<=0.1, metric.loss:>=0.4` will match all entities that have a metric outside the range 0.1 and 0.4

You can of course use any combination of the operators and with negation modifier.


## Query with value condition

This is useful to compare categorical values, e.g. statuses, search algorithm, ids, commit hash, ...
you can search for values that are equal, not equal, in a set of values, or not in a set of values.


operator               | example
-----------------------|------------------
`x = y`                | `status: running` will match all entities that have the status running
`x != y`               | `status: running` will match all entities that have the status not running
`x in {a, b, c}`       | `status: started|building|running` will match all entities that have the status in one of the values started, building, or running
`x not in {a, b, c}`   | `status: ~started|building|running` will match all entities that have the status not in one of the values started, building, or running


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

## Query with the negation modifier

You can negate any condition by prefixing the query with `~`, e.g `x:~2` is the equivalent of saying is different than 2.

## Query by combining multiple conditions

Every time you put a comma `,` Polyaxon will filter further  by the condition that comes after the comma.


## Entities

 * [Builds](entities/builds)
 * [Jobs](entities/jobs)
 * [Tensorboards](entities/tensorboards)
 * [Experiments](entities/experiments)
 * [Experiment groups](entities/experiment_groups)
