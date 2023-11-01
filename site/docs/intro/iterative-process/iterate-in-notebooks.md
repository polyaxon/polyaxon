---
title: "Iterate in notebooks"
sub_link: "iterative-process/iterate-in-notebooks"
meta_title: "Notebooks Iteration - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Notebooks Iteration - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - notebook
  - quick-start
sidebar: "intro"
---

![notebooks](../../../../content/images/concepts/dashboard/notebooks.png)

We previously learned how to create components and how to have more control over the scheduling process using operations.
In this sections we will learn how to run components interactively inside a Jupyter notebook.

> Same principle applies to running other interactive environments, e.g. vscode session, zeppelin, or any other service.

## Overview

[Notebooks](https://jupyter.org/) allow users to create and share documents that contain live code,
visualizations and explanatory texts.
Notebooks are great for interactively writing and debugging your code and visualizing your results and data.

## Start a notebook

Starting a notebook is similar to running any other Polyaxon components, i.e. we need to define a Polyaxonfile or use a public component.

Let's run one of the public notebook components:

```bash
polyaxon run --hub jupyterlab:tensorflow -w
```

> For more details about this command please run `polyaxon run --help`, or check the [command reference](/docs/core/cli/run/)

Since the notebook is created with a Polyaxonfile, it can be customized similar to as any other job or service, e.g. instead of just executing `polyaxon run`
we can create an operation to customize the environment, request GPUs, define termination ... when a predefined public component is limiting users can create their own component:

```yaml
version: 1.1
kind: operation
hubRef: jupyterlab:tensorflow
runPatch:
  container:
    resources:
      requests:
        cpu: 200m
        gpu: 1
        memory: 512
      limits:
        cpu: 1
        gpu: 1
        memory: 2048
```

## Stop a notebook

We stop a notebook the same way we stop any other operation, run the following command in your terminal:

If the operation is cached

```bash
polyaxon ops stop
```

Otherwise, you need to pass a UUID

```bash
polyaxon ops -uid UUID stop
```

> For more details about this command please run `polyaxon ops --help`, or check the [command reference](/docs/core/cli/ops/)

You can also start and stop notebooks, and any other operation from the UI.


## Resume a notebook

Resuming a notebook is similar to resuming any other operations:


If the operation is cached

```bash
polyaxon ops resume
```

Otherwise, you need to pass a UUID

```bash
polyaxon ops -uid UUID resume
```

## Start experiments

We need to install polyaxon in our Jupyter environment:

```bash
!pip install -U polyaxon
```

We will programmatically schedule some experiments from the notebook, all experiments that we schedule from the notebook will run inside isolated pods in the Kubernetes cluster.
Each one of those experiments will be managed separately by Polyaxon and will create a new record under the runs table in the database.

```python
from polyaxon.tuners.grid_search import GridSearchManager
from polyaxon.schemas import V1GridSearch, V1HpChoice, V1HpLinSpace
from polyaxon.client import RunClient

client = RunClient()

grid_search_config = V1GridSearch(
    params={"optimizer": V1HpChoice(value=["adam", "sgd", "rmsprop"]),
            "dropout": V1HpLinSpace(value={'num': 20, 'start': 0.1, 'stop': 0.5}),
            "epochs": V1HpChoice(value=[5, 10])},
    num_runs=5
)

suggestions = GridSearchManager(grid_search_config).get_suggestions()
for suggestion in suggestions:
    client.create_from_url(
        url="https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yaml",
        params=suggestion)
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

Get metrics for a specific run

```python
from polyaxon.client import RunClient
run_client = RunClient()
run_client.get_metrics(['loss', 'accuracy'])
```

Tidy dataframe

```python
run_client.get_metrics_as_tidy_df()
```

Install some plotting dependencies

```yaml
!pip install plotly hiplot
```

If you are using Jupyter notebook you can skip this step, otherwise, to use Plotly Express in JupyterLab,
you will need to install the express extension (mode details can be found [in Plotly troubleshooting page](https://plotly.com/python/troubleshooting/#jupyterlab-problems)), in a new terminal run and reload the notebook:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyterlab-plotly
```

Plot a line chart

```python
run_client.get_metrics_as_line_chart()
```

Example in notebook:

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-plotly-tidy.png)

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-plotly-metric.png)

Let's compare several runs:

```python
from polyaxon.client import RunClient

client = RunClient()
# This is an example of getting top 100 based on loss of all experiment
# that have one of the tags experiment or examples
hiplot_experiment = client.get_runs_as_hiplot(query="tags:experiment|examples", sort="-metrics.loss", limit=100)
hiplot_experiment.display()
```

Example in notebook:

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-hiplot1.png)

![run-dashboards-hiplot2](../../../../content/images/dashboard/runs/programmatic-hiplot2.png)
