# Searching Experiment Groups

## Query

field                         | condition
------------------------------|------------------
`created_at`                  | [datetime condition](/query_syntax/introduction/#query-with-datetime-condition)
`updated_at`                  | [datetime condition](/query_syntax/introduction/#query-with-datetime-condition)
`started_at`                  | [datetime condition](/query_syntax/introduction/#query-with-datetime-condition)
`finished_at`                 | [datetime condition](/query_syntax/introduction/#query-with-datetime-condition)
`user.id`                     | [value condition](/query_syntax/introduction/#query-with-value-condition)
`user.username`               | [value condition](/query_syntax/introduction/#query-with-value-condition)
`project.*` (e.g. project.id) | [value condition](/query_syntax/introduction/#query-with-value-condition)
`name`                        | [value condition](/query_syntax/introduction/#query-with-value-condition)
`status`                      | [value condition](/query_syntax/introduction/#query-with-value-condition)
`tags`                        | [value condition](/query_syntax/introduction/#query-with-value-condition)
`search_algorithm`            | [value condition](/query_syntax/introduction/#query-with-value-condition)
`concurrency`                 | [comparison condition](/query_syntax/introduction/#query-with-comparison-condition)


## Sort

field:

 * `created_at`
 * `updated_at`
 * `started_at`
 * `finished_at`
