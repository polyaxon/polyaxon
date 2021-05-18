---
title: "Comparing runs with Tensorboard"
sub_link: "tensorboard/comparing-runs-tensorboard"
meta_title: "Comparing runs with Tensorboard - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Starting Tensorboard based on run uuids - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

In previous sections we started several experiments, we also learned how to start a Tensorboard service to visualize a single experiment. 
In this section we will start a tensorboard to visualize and compare a selection of experiments.

## Listing experiments

Polyaxon provides several ways to list runs, using the UI with the comparison table, using the API, or using the CLI.

Let's use the CLI to show the current runs under a specific project:

```bash
polyaxon ops ls [-p PROJECT_NAME]
```

This command will show all runs created under a specific project, it will also show both service, job, dag, and matrix runs, and it will provide a mechanism for paginating the records.
We can reduce the information in this list by providing a [query](/docs/core/query-language/) similar to the UI.

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 5
```

The flags `--query/-q`, `--sort/s`, and `--limit/-l` allows to restrict the list based on the query specification, order by fields, and a limit. 

You may notice that the list does not show important columns like metrics or params, we can add `-io` flag to show all inputs and outputs:

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 5 -io
```

Now we have way too many columns, we can do better by providing what columns to show using `-c "column1, column2, ..."`, for instance let's just show the `uuid`, `learning_rate`, `loss` and `accuracy`.

```bash
polyaxon ops ls [-p PROJECT_NAME] -q "kind: job, metrics.loss: <0.3" -s "-metrics.loss" -l 5 -io -c "uuid,in.learning_rate,out.loss,out.accuracy" 
```

## Starting a Tensorboard for multiple runs

We were able to query, sort, and limit our runs, let's try to start a Tensorboard service for the top 5 experiments based on `loss`. We need to pass the uuid values of those runs to the Tensorboard component:

```bash
polyaxon run --hub [-p PROJECT_NAME] tensorboard:multi-run -P uuids=UUID1,UUID2,UUID3,UUID4,UUID5
```

You will notice that this command is almost the same as the previous command for starting a single run Tensorboard, the only difference is that we are using a different `tag` for the `tensorboard` component.
We are also passing a different parameter `uuids` that this tag is expecting.

## Start Tensorboard directly from the artifacts store

> **Note**: Requires Polyaxon v1.9.1 or higher.

When one or multiple experiments are still running the previous command is not very useful because it only loads the latest snapshot of the experiments' outputs.

If you deployed Polyaxon with S3/GCS/Volume artifacts store, you can also point the Tensorboard directly to the artifacts store path instead of the Polyaxon's context.

```bash
polyaxon run --hub tensorboard:multi-run-storepath -P uuids=UUID1,UUID2,UUID3,UUID4,UUID5
```

> **Note**: This component version will not work with Azure or other artifacts store backend, because Tensorboard does not load the outputs natively from those services.   


## Starting a Tensorboard for multiple runs from the UI

On Polyaxon Cloud or Polyaxon EE, when a user selects several runs in the comparison table, a button called `custom action` appears, it allows to provide a component to run based on the selection.
Users can use `tensorboard:multi-run` or `tensorboard:multi-run-storepath` to start a new Tensorboard based on that selection.
