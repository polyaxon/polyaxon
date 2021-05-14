---
title: "Native Charts"
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

Polyaxon dashboard provides several visualizations and charts based on events logged by the [tracking API](/docs/experimentation/tracking/).

## Single runs:

![run-dashboards](../../../../content/images/dashboard/runs/dashboards.png)

 * Line charts
![run-dashboards-lines](../../../../content/images/dashboard/runs/dashboards-lines.png)

![run-dashboards-lines](../../../../content/images/dashboard/runs/dashboards-many.png)

 * Bar charts

![run-dashboards-lines](../../../../content/images/dashboard/runs/dashboards-bars.png)

 * Stats charts

![run-dashboards-lines](../../../../content/images/dashboard/runs/dashboards-stats.png)

 * Histogram charts
 * Curve charts: PR curves, AUC/ROC curves, custom curves (<x, y> arrays)

![run-dashboards-pr-curve](../../../../content/images/dashboard/runs/dashboard-pr-curve.png)

![run-dashboards-roc-curve](../../../../content/images/dashboard/runs/dashboards-roc-curve.png)

## Multi-run

For multi-run you can compare metrics and curves from several runs, as well as charts for hyperparameter values and metrics:

![runs-comparison-new](../../../../content/images/dashboard/comparison/charts-new.png)

![runs-comparison-many](../../../../content/images/dashboard/comparison/charts-many.png)

 * Line charts

![runs-comparison-lines](../../../../content/images/dashboard/comparison/charts-lines.png)

 * Bar charts

![runs-comparison-bars](../../../../content/images/dashboard/comparison/charts-bars.png)

 * Stats charts

![runs-comparison-stats](../../../../content/images/dashboard/comparison/charts-stats.png)

 * Curve charts: PR curves, AUC/ROC curves, custom curves (<x, y> arrays)

![runs-comparison-pr-curves](../../../../content/images/dashboard/comparison/charts-pr-curves.png)

![runs-comparison-roc-curves](../../../../content/images/dashboard/comparison/charts-roc-curves.png)

 * Scatter charts

![runs-comparison-scatter](../../../../content/images/dashboard/comparison/charts-scatter.png)

 * Parallel coordinates
 * Contour plots

![runs-comparison-multi](../../../../content/images/dashboard/comparison/charts-multi.png)

## Media rendering

Polyaxon can render several media types, you can log several versions of the same media with step index:

 * images
 * text
 * html
 * audio
 * video
 * dataframe
