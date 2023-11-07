---
title: "Run Logs"
sub_link: "runs-dashboard/logs"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Run Logs"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

Polyaxon comes with a powerful and uniform logging experience for all runs.

The logging features collects and archives logs for all your containers inside a run, and even from distributed runs, experiments, jobs, notebooks, tensorboards, …
all runs have a similar logging experience, which helps users detect issues related to why a tensorboard is not loading or a notebook is not accessible.

## Logs in CLI

You can stream logs from the CLI or from the UI, which will reduce the need to reach out for Kubernetes to check per container issues

![run-logs-cli](../../../../content/images/dashboard/runs/logs-cli.png)

## Logs in UI

You can stream logs in the dashboard as well with support for progress bars, ANSI standards, and long log lines.

![run-logs-dark](../../../../content/images/dashboard/runs/logs-dark.png)

It’s possible to hide/show information about nodes, pods, and containers,
this is especially important for distributed runs, or restarts.

![run-logs-filter](../../../../content/images/dashboard/runs/logs-filter.png)

And you can sort logs by latest timestamp first and keep streaming new logs to avoid scrolling to the bottom.

![run-logs-sort](../../../../content/images/dashboard/runs/logs-sort.png)

> It’s also possible to disable logs storage for a specific experiment or based on a specific tag, e.g. users might want to avoid storing logs for debug jobs.
