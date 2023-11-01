---
title: "Runs Graph"
sub_link: "runs-dashboard/graph"
meta_title: "Polyaxon management tools and UI - Runs dashboard - Runs Graph"
meta_description: "Polyaxon runs dashboard for Machine learning experiment tracking and visualizations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

The graph view is a powerful tool for listing, filtering, and comparing runs of all kinds under the same pipeline following their dependencies.


## Feature

The graph view provides similar features as the timeline view, but instead of showing a table it shows a dependency graph, you can zoom in, zoom out, fit the graph, and open operations in flyout :

![graph-flyout](../../../../content/images/dashboard/graph/graph-flyout.png)

The graph view comes with two direction:

 * `right` direction for deep graphs

![graph-deep](../../../../content/images/dashboard/graph/graph-deep.png)

 * `down` direction for wide graphs

![graph-wide](../../../../content/images/dashboard/graph/graph-wide.png)

When hovering an operation, the upstream edges are colored based on the status of the upstream operations

![graph-hover1](../../../../content/images/dashboard/graph/graph-hover1.png)

If an operation fails you can see all operations that contributed to the `upstream-failed` status:

![graph-hover1](../../../../content/images/dashboard/graph/graph-hover2.png)
