---
title: "Run Info"
sub_link: "runs-dashboard/info"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Run Info"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

Every time you run a component whether it contains a machine learning model training, a tensorboard, a hyperparameter optimization, or a workflow,
Polyaxon will log that execution as a run and connection any information related to it, e.g. params, artifacts, upstream/downstream runs, ...

## Overview

All runs in Polyaxon has some similar characteristics, based on the [component/operation specification](/docs/core/specification/):
   * name, description, and tags
   * inputs/outputs

![run-overview](../../../../content/images/dashboard/runs/overview1.png)

![run-overview](../../../../content/images/dashboard/runs/overview2.png)
