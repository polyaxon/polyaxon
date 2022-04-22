---
title: "Searches"
sub_link: "organizations/searches"
meta_title: "Polyaxon management tools and UI - Searches"
meta_description: "Saved searches let you save and describe search queries, for your experiments, jobs, and builds."
visibility: public
status: published
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>


If your projects have a large number of runs, and you only need to compare a subset of these runs, you can use filters.

A search allows to:
 * Compare parameters and metrics of the runs using the search filters.
 * Create visualizations of the runs based on the search filters.
 * Create a tensorboard showing only top experiments using the search filters.
 * Have quick access to the runs using the search filters.

Oftentimes, a search might be useful to save and reuse to quickly filter all runs.
Saved searches let you save and describe a query, sort condition, columns order and selection, fields heat configuration ...
You can easily then monitor the results on an ongoing basis and find the desired results easily.

> We are also working on Alerts for saved searches so that you can subscribe and get notified based on specific conditions, or trigger an operation or a workflow.

## Examples of useful searches

### Recent finished runs

 * query: `status: succeeded | failed | stopped`
 * sort: `-finished_at`

### Best performing experiments based on specific metrics:

 * query: `metrics.loss: <=0.3, metrics.precision: >=0.89`
 * sort: `metrics.loss, -metrics.precision`

### Experiment with specific code commit:

 * query: `commit: COMMIT-HASH`


## Create saved searches

A saved search consists of a name (must be a slug) describing the search, and query/sort based on the specification.

Saved searches are created on the project level, only users having write access to the project can create a search,
and they can be used by any user who has read access to the project.

![search-create](../../../../content/images/dashboard/searches/create.png)


## Select saved searches

You can access all saved searches on the current project and on the organization level.

![search-select](../../../../content/images/dashboard/searches/select.png)

## Manage saved searches

You can manage, update, delete searches on the project level, and promote them to the organization level.

![search-manage](../../../../content/images/dashboard/searches/manage.png)
