---
title: "Single Run Tensorboard"
sub_link: "tensorboard/single-tensorboard"
meta_title: "Single Tensorboard - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Starting Single Run Tensorboard - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

In the first quick start tutorial, we created a single run and started Tensorboard service to visualize the outputs.

In this tutorial we will explore a couple more options to start Tensorboard services for single experiments.

## Start a Tensorboard

To start a Tensorboard for a specific run:

```bash
polyaxon run --hub tensorboard:single-run -P uuid=UUID
```

This component version will load the outputs and prepare them for a Tensorboard service. This is usually useful for finished experiments.

## Start Tensorboard directly from the artifacts store

> **Note**: Requires Polyaxon v1.9.1 or higher.

When an experiment is still running the previous command is not very useful because it only loads the latest snapshot of the experiment's outputs.

If you deployed Polyaxon with S3/GCS/Volume artifacts store, you can also point the Tensorboard directly to the artifacts store path instead of the Polyaxon's context.

```bash
polyaxon run --hub tensorboard:single-run-storepath -P uuid=UUID -w
```

> **Note**: This component version will not work with Azure or other artifacts store backend, because Tensorboard does not load natively the outputs from those services.   

## Start Tensorboard from the UI

If you are using Polyaxon Cloud or Polyaxon EE, you can perform the same actions using the UI.
Polyaxon tracks runs that have Tensorboard as one of their artifacts and shows a button to start or resume a Tensorboard service for those runs.
