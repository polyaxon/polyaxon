---
title: "Run Resources"
sub_link: "runs-dashboard/monitoring"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Run Resources"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

Polyaxon has an automatic tracking of run events to provide a uniform observability and monitoring for resources as well as statuses, events, and conditions of all runs.

## Statuses

Run status is at the heart of every run. It is used to represent the current state of an experiment or a notebook, and helps users to view passed stages of a run.

Polyaxon has now features for observability and monitoring for resources as well as statuses, events, and conditions.

The CLI has a command argument `--watch -w` for watching statuses and events in real-time, same with the UI,
it streams the statuses and provides much deeper insight about the conditions of the underlying pods.

![run-statuses](../../../../content/images/dashboard/runs/statuses.png)

You can get instant information about any run's lifecycle and stage:

![run-statuses-light](../../../../content/images/dashboard/runs/statuses-light.png)

## Resources

You can enable resources tracking for your experiment to log MemCPU/GPU resource consumption

![run-resources](../../../../content/images/dashboard/runs/resources.png)

![run-resources2](../../../../content/images/dashboard/runs/resources2.png)
