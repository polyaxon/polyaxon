---
title: "Hiplot"
meta_title: "Hiplot"
meta_description: "Polyaxon comes with a Hiplot integration to analyze multiple experiments."
custom_excerpt: "HiPlot is a lightweight interactive visualization tool to help AI researchers discover correlations and patterns in high-dimensional data using parallel plots and other graphical ways to represent information."
image: "../../content/images/integrations/hiplot.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
  - visualizations
featured: false
popularity: 1
class_name: instruction
visibility: public
status: published
---

Polyaxon comes with a [Hiplot](https://facebookresearch.github.io/hiplot/index.html) integration to analyze multiple experiments.

## Tracking

You can track hyperparameter and metrics of your experiments using [Polyaxon's tracking module](/docs/experimentation/tracking/module).

## In notebooks

You can use the module [MultiRunPlot](/docs/experimentation/visualizations/programmatic/#hiplot) which requires hiplot to create interactive parallel coordinates inside a notebook or jupyter lab.

## Example

```python
from polyaxon.client import RunClient

client = RunClient()
exp = client.get_runs_as_hiplot(query="metrics.loss:<0.1")
exp.display()
```

![run-dashboards-hiplot1](../../content/images/dashboard/runs/programmatic-hiplot1.png)

![run-dashboards-hiplot2](../../content/images/dashboard/runs/programmatic-hiplot2.png)
