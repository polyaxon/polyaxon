---
title: "Using the CLI"
sub_link: "query-metadata-artifacts/using-cli"
meta_title: "Introduction to Querying Metadata and Artifacts Using the CLI - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Introduction to Querying Metadata and Artifacts Using the CLI - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Search runs

Before we perform any search, we will first query the runs in our current project:

```bash
polyaxon ops ls [-p PROJECT_NAME]
```

This command will show us the current runs inside our project. 
Note that by default the CLI will show a table of `20` runs and will automatically show to paginate the full history.

We can filter the results based on a specific metric. 
The flags `--query/-q`, `--sort/-s`, `--offset/-off`, and `--limit/-l` allows to restrict the list based on the query specification, order by fields, and to limit or offset the results.

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 3
``` 

You may notice that the list does not show important columns like metrics or params, we can add `-io` flag to show all inputs and outputs:

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 3 -io
```

Now we have way too many columns, we can do better by providing what columns to show using `--columns/-c`, e.g. `-c "column1, column2, ..."`, for instance let's just show the `uuid`, `learning_rate`, `loss` and `accuracy`.

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 3 -io -c "uuid,in.learning_rate,out.loss,out.accuracy" 
```

## Persisting the search results to a CSV file

We can save the search above to a CSV file by adding the flag `--to-csv`.

For example we can save the full table: 

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 3 -io --to-csv
```

Or the filtered table:

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 3 -io -c "uuid,in.learning_rate,out.loss,out.accuracy" --to-csv 
```

## Getting more information about the runs 

In order to view and explore the top runs, we can query information about a specific run using the `-uid`, 
for example if the first run has uuid value `8aac02e3a62a4f0aaa257c59da5eab80` we can query the run's information with CLI:

```bash
polyaxon ops get -uid 8aac02e3a62a4f0aaa257c59da5eab80 [-p PROJECT_NAME]
```

## Downloading artifacts for single runs

Polyaxon provides a command `artifacts` to download the assets stored in run. 
Note that you can add `[-p/--project PROJECT_NAME] [--path-to/--path PATH]` to the following commands to specify the project and path where the artifacts should be stored.

 * All artifacts

```bash
polyaxon ops artifacts -uid 8aac02e3a62a4f0aaa257c59da5eab80
```
  
 * Specific file(s) based on a path using `-f/--file`

```bash
polyaxon ops artifacts -uid 8aac02e3a62a4f0aaa257c59da5eab80 -f "outputs/path/file1" -f "outputs/path2/file2"
```

 * Specific directory(ies) based on a path using `-d/--dir`

```bash
polyaxon ops artifacts -uid 8aac02e3a62a4f0aaa257c59da5eab80 -d "outputs/path/dir1" -d "outputs/pat2/dir2"
```

 * Specific artifacts based on the lineage reference name using `-l-name/--lineage-name`
 
```bash
polyaxon ops artifacts -uid 8aac02e3a62a4f0aaa257c59da5eab80 -l-name image-example -l-name debug-csv-file
```

* Specific artifacts based on the lineage reference kind using `-l-kind/--lineage-kind`
 
```bash
polyaxon ops artifacts -uid 8aac02e3a62a4f0aaa257c59da5eab80 -l-kind model -l-kind env
```

## Pulling metadata and artifacts for single runs

You can package and download the metadata, lineage metadata, and artifacts using the `pull` command.
Note that you can add `[-p/--project PROJECT_NAME] [--path-to/--path PATH]` to the following commands to specify the project and path where the data should be stored.

 * Pulling the metadata and lineage only

```bash
polyaxon ops pull -uid 8aac02e3a62a4f0aaa257c59da5eab80 --no-artifacts
```

 * Pulling the metadata, lineage metadata, and artifacts

```bash
polyaxon ops pull -uid 8aac02e3a62a4f0aaa257c59da5eab80
```

## Pulling metadata and artifacts for all the top runs

Instead of pulling data for each run, we can using the same query specification above to archive all the best runs:

```bash
polyaxon ops pull -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 3
```

