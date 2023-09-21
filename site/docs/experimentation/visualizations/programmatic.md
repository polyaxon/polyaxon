---
title: "Programmatic Experience"
sub_link: "visualizations"
meta_title: "Visualization in Polyaxon - Experimentation"
meta_description: "Polyaxon comes with a powerful and customizable visualization system for driving visualization in the dashboard or programmatically."
tags:
  - concepts
  - polyaxon
  - experimentation
  - experiments
  - architecture
sidebar: "experimentation"
---

## Overview

Polyaxon has a programmatic experience for generating visualizations for single runs or multi-run:

## Single run

You can use the module `Polyplot` which requires `Plotly express` to drive visualizations inside a notebook or jupyter lab.

the module comes with functions to load events, and visualize them:

```python
from polyaxon.client import RunPlot

client = RunPlot(run_uuid="...")
client.get_metrics(names="loss,accuracy")
client.line()
client.bar()
...
```

![run-dashboards-df-tidy](../../../../content/images/dashboard/runs/programmatic-plotly-tidy.png)

![run-dashboards-metric](../../../../content/images/dashboard/runs/programmatic-plotly-metric.png)

## HiPlot

You can use the module `MultiRunPlot` which requires `hiplot` to create interactive parallel coordinates inside a notebook or jupyter lab.


```python
from polyaxon.client import RunClient

client = RunClient()
exp = client.get_runs_as_hiplot(query="metrics.loss:<0.1")
exp.display()
```

![run-dashboards-hiplot1](../../../../content/images/dashboard/runs/programmatic-hiplot1.png)

![run-dashboards-hiplot2](../../../../content/images/dashboard/runs/programmatic-hiplot2.png)
