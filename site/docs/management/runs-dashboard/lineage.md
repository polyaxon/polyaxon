---
title: "Run Lineage"
sub_link: "runs-dashboard/lineage"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Run Lineage"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

Polyaxon UI tracks additional information about your artifacts and runs dependencies.

## Overview

The dashboard comes with a lineage tab with deeper information about inputs and outputs artifacts, with special handling for several types: git, dockerfiles, files, events, metrics, …

The dashboard shows also any dependent jobs, experiments, and services, if an experiment was restarted, resumed, information about the upstream and downstream operations.

![run-lineage](../../../../content/images/dashboard/runs/lineage.png)

The lineage UI is also directly linked to the model registry and the workflow managers.
