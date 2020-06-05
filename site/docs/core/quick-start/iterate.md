---
title: "Quick Start: Iterate"
sub_link: "quick-start/iterate"
meta_title: "Notebooks Iteration - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Operations - Get started with Polyaxon and become familiar with the ecosystem of Polyaxon with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - notebook
    - quick-start
sidebar: "core"
---

![notebooks](../../../../content/images/concepts/dashboard/notebooks.png)

We previously learned how to create components and how to run them using operations. 
In this section we will learn how to run components interactively inside a Jupyter notebook.

> Same principle applies to running other interactive environments, e.g. zeppelin, or any other service.  

## Overview

[Notebooks](https://jupyter.org/) allow users to create and share documents that contain live code,
visualizations and explanatory texts.

Notebooks are great for interactively writing and debugging your code and visualizing your results and data.

## Start a notebook

Starting notebook is similar to running any other Polyaxon components, i.e. you need to define polyaxonfile or use a public component.

Let's run one of the public notebook components:

```bash
$ polyaxon run --hub jupyter-lab:tensorflow -w
```

> For more details about this command please run `polyaxon run --help`, 
or check the [command reference](/docs/core/cli/run/)

Since the notebook is created with a polyaxonfile, it can be customized in the same way as any other job, e.g. instead of just executing `polyaxon run` 
we can create an operation to customize the resources, request GPUs ... in case the component itself is limiting, users can create their own component:

```yaml
version: 1.1
kind: operation
hubRef: jupyter-hub:tensorflow
runPatch:
  container:
    resources:
      cpu:
        requests: 2
        limits: 4
      gpu:
        requests: 1
        limits: 1
      memory:
        requests: 512
        limits: 2048
```

## Stop a notebook

You stop a notebook the same way you stop any other operation, run the following command in your terminal:

If the operation is cached

```bash
$ polyaxon ops stop
```

Otherwise you need to pass a UUID

```bash
$ polyaxon ops -uid UUID stop
```

> For more details about this command please run `polyaxon ops --help`, 
or check the [command reference](/docs/core/cli/ops/)

> You can also start and stop notebooks, and any other operation from the UI. 


## Start experiments

We will programmatically run some experiments inside the notebook:

```python
from polyaxon.polytune.search_managers.grid_search.manager import GridSearchManager
from polyaxon.polyflow import V1GridSearch, V1HpChoice, V1HpLinSpace
from polyaxon.client import RunClient

client = RunClient()

grid_search_config = V1GridSearch(
    params={"optimizer": V1HpChoice(value=["adam", "sgd", "rmsprop"]), "dropout": V1HpLinSpace(value={'num': 20, 'start': 0.1, 'stop': 0.5})},
    num_runs=5
) 

suggestions = GridSearchManager(grid_search_config).get_suggestions()
for suggesion in suggestions:
    client.create_from_url(url="https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/simple.yml", params=suggesion)
```


## Analyze the experiments

Let's try to derive some insights from the experiments.

Let get the top experiment:

```python
from polyaxon.client import RunClient

client = RunClient()
run = client.list(sort="-metrics.loss", limit=1).results[0]
run_client = RunClient(run_uuid=run.uuid)
run_client.refresh_data()
print(run_client.get_inputs())
print(run_client.get_outputs())
```

Example in notebook:

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-plotly-tidy.png)

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-plotly-metric.png)

Let's compare runs:

```python
from polyaxon.polyplot import MultiRunPlot

client = MultiRunPlot()
# This is an example of getting top 100 based on loss of all experiment 
# that have one of the tags experiment or examples 
hiplot_experiment = client.get_hiplot(query="metrics.tags:experiment|examples", sort="-metrics.loss", limit=100)
hiplot_experiment.display()
```

Example in notebook:

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-hiplot1.png)

![run-dashboards-hiplot2](../../../../content/images/dashboard/runs/programmatic-hiplot2.png)
