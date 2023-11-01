---
title: "Runs Timeline"
sub_link: "runs-dashboard/timeline"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Runs Timeline"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

The timeline view is a powerful tool for listing, filtering, and comparing runs of all kinds under the same pipeline following their start date and their duration.


## Features

The timeline view give similar features as the comparison table, and adds a Gantt chart to produce a visual timeline of all runs.

![timeline-tune](../../../../content/images/dashboard/timeline/timeline-tune.png)

The timeline view is powerful when you have a pipeline with nested DAGs or contains a mix of operations (jobs, hyperparams tuning jobs, services).

![timeline-dag](../../../../content/images/dashboard/timeline/timeline-dag.png)

It can be useful as well to view the progress of a schedule or a cron

![timeline-schedule](../../../../content/images/dashboard/timeline/timeline-schedule.png)
