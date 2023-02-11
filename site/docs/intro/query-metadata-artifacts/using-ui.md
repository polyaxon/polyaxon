---
title: "Using the UI"
sub_link: "query-metadata-artifacts/using-ui"
meta_title: "Introduction to Querying Metadata and Artifacts Using Polyaxon the UI - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Introduction to Querying Metadata and Artifacts Using Polyaxon the UI - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

The UI's runs table provides the interface to interact with the runs started by the scheduling logic or logged using the tracking module.
It has several features for filtering, sorting, comparing, and visualizing the runs history:

![table-search-runs](../../../../content/images/dashboard/query-metadata-artifacts/table-search-runs.png)

## Search runs

Before we perform any search, we will first query the runs in our current project:

![list-runs](../../../../content/images/dashboard/query-metadata-artifacts/list-runs.png)

This command will show us the current runs inside our project.

We can filter the results based on a specific metric, we can also show the columns we are interested by and color them:

![filter-runs](../../../../content/images/dashboard/query-metadata-artifacts/filter-runs.png)

## Persisting the search results to a CSV file

The search configuration above can be saved to a CSV file by clicking the `Actions` button

![runs-table-csv](../../../../content/images/dashboard/query-metadata-artifacts/runs-table-csv.png)

## Getting more information about the runs

In order to view and explore the runs in the table, we can view each run in the flyout mode:

![run-info](../../../../content/images/dashboard/query-metadata-artifacts/run-info.png)

## Downloading artifacts for single runs

Polyaxon provides an `artifacts` tab to view, navigate, render, and download the artifacts:

 * All artifacts

![run-download-artifacts](../../../../content/images/dashboard/query-metadata-artifacts/run-download-artifacts.png)

 * Specific file or dir based on a path

![run-download-path](../../../../content/images/dashboard/query-metadata-artifacts/run-download-path.png)

 * Specific artifacts based on the lineage

![run-download-lineage](../../../../content/images/dashboard/query-metadata-artifacts/run-download-lineage.png)
