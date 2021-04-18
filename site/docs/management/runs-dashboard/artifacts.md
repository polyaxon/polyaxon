---
title: "Run Dashboards"
sub_link: "runs-dashboard/dashboards"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Run Dashboards"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

Polyaxon allows to track several artifacts. The outputs page in the UI allows to download single artifacts, subpaths or pull everything
that was stored in the artifacts store for a specific run.

> The same experience is also possible through the API and the Python client.

![run-artifacts](../../../../content/images/dashboard/runs/artifacts.png)

## Rendering

The artifacts tab allows you to render text files

![run-artifacts-file](../../../../content/images/dashboard/runs/artifacts-code.png)

It also detects programming language to render the code editors for code files

![run-artifacts-file-dark](../../../../content/images/dashboard/runs/artifacts-code-dark.png)

## Media

The artifacts tab has also an enhanced filetype detection with proper rendering for media.

![run-artifacts-audio](../../../../content/images/dashboard/runs/artifacts-audio.png)

All widgets have a fullscreen mode and the possibility to download the artifact/asset.

![run-artifacts-image](../../../../content/images/dashboard/runs/artifacts-image.png)
