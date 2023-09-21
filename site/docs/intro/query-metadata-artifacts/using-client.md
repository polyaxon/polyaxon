---
title: "Using the Client"
sub_link: "query-metadata-artifacts/using-client"
meta_title: "Introduction to Querying Metadata and Artifacts Using Polyaxon the Client - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Introduction to Querying Metadata and Artifacts Using Polyaxon the Client - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
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

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME")
response = run_client.list()
print("Count: {}".format(response.count))
print("Next page: {}".format(response.next))
# Runs in this page
runs = response.results
```

The list method shows the current runs inside our project.
Note that by default the Client will show a table of `20` runs and have `previous` and `next` to paginate the full history.

We can filter the results based on a specific metric.
The params `query`, `sort`, `offset`, and `limit` allows to restrict the list based on the query specification, order by fields, and to limit or offset the results.

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME")
response = run_client.list(query="kind: job, metrics.loss: <0.3", sort="-metrics.loss", limit=3)
runs = response.results
```

We can for instance iterate over the runs to show some details:

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME")
response = run_client.list(query="kind: job, metrics.loss: <0.3", sort="-metrics.loss", limit=3)
runs = response.results
for r in runs:
    print({"uuid": r.uuid, "learning_rate": r.inputs.get("learning_rate"),
           "loss": r.outputs.get("loss"), "accuracy": r.outputs.get("accuracy")})
```

## Getting more information about the runs

In order to view and explore the top runs, we can query information about a specific run using the `run_uuid`,
for example if the first run has uuid value `8aac02e3a62a4f0aaa257c59da5eab80` we can query the run's information with CLI:

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")

# All run data
print(run_client.run_data)

# Inputs
print(run_client.get_inputs())

# Outputs
print(run_client.get_outputs())

# Lineage metadata
print(run_client.get_artifacts_lineage())

# Statuses history
print(run_client.get_statuses())
```

## Downloading artifacts for single runs

The Python Client provides methods to filter and download the assets, events, and artifacts for each run.

 * List artifacts tree

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
# Root path
print(run_client.get_artifacts_tree())
# Specific path
print(run_client.get_artifacts_tree(path="outputs"))
```

 * Download all artifacts

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
run_client.download_artifacts()
```

 * Specific file based on a path using `download_artifact` and specifying the path

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
run_client.download_artifact(path="outputs/path/file1")
```

 * Specific directory based on a path using `download_artifacts`  and specifying the path

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
run_client.download_artifacts(path="outputs")
```

 * Specific artifacts based on the lineage reference name

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
lineages = run_client.get_artifacts_lineage(query="name: image-example | debug-csv-file").results

for lineage in lineages:
    run_client.download_artifact_for_lineage(lineage=lineage)
```

* Specific artifacts based on the lineage reference kind

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
lineages = run_client.get_artifacts_lineage(query="kind: model | env").results

for lineage in lineages:
    run_client.download_artifact_for_lineage(lineage=lineage)
```

## Pulling metadata and artifacts for single runs

You can package and download the metadata, lineage metadata, and artifacts using the `pull` method.

 * Pulling the metadata and lineage only

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
run_client.pull_remote_run(path="/tmp/save/to/path", download_artifacts=False)
```

 * Pulling the the metadata, lineage metadata, and artifacts

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME", run_uuid="8aac02e3a62a4f0aaa257c59da5eab80")
run_client.pull_remote_run(path="/tmp/save/to/path", download_artifacts=True)
```

## Pulling metadata and artifacts for all top runs

Instead of pulling data for each run, we can using the same query specification above to archive all the best runs:

```python
from polyaxon.client import RunClient

run_client = RunClient(project="PROJECT_NAME")
response = run_client.list(query="kind: job, metrics.loss: <0.3", sort="-metrics.loss", limit=3)
# Runs in this page
runs = response.results
for r in runs:
    r_client = RunClient(project="PROJECT_NAME", run_uuid=r.run_uuid)
    r_client.pull_remote_run(path="/tmp/save/to/path/{}".format(r.uuid), download_artifacts=True)
```
