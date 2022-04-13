---
title: "Querying Metadata & Artifacts"
sub_link: "query-metadata-artifacts"
meta_title: "Introduction to Querying Metadata and Artifacts - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Introduction to Querying Metadata and Artifacts - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
is_index: true
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

Polyaxon provides a [query language](/docs/core/query-language/) to search and filter the runs history. 
Using the API, Client, CLI or UI user can perform searches and find the runs with important information or to compare results. 
Additionally, all metadata, assets, events, and artifact logged during a run can be queried and downloaded to a local path. 

By leveraging the query specification and download interfaces, you can:

 * Build custom analyses or visualizations
 * Pull saved model checkpoints
 * Download code or uploaded artifacts
 * Move a run or several from one instance to another
 * Package and share results outside Polyaxon 

## Searching runs

In the previous sections of this tutorial we started several runs, with different hyperparameters or different logic.
In this section we will:

 * Search the runs history based on a metric
 * Limit the search to the top 3 runs
 * Explore runs metadata
 * Download artifacts
 * Persist the metadata and artifact of a single run and the 3 top runs
