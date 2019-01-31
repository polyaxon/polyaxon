---
title: "Polyaxon Saved searches"
sub_link: "polyaxon-query-syntax/saved-searches"
meta_title: "Polyaxon Saved searches - Polyaxon References"
meta_description: "Saved searches lets you save and describe search queries, for your groups, experiments, jobs, and builds."
visibility: public
status: published
tags:
    - query
    - reference
    - polyaxon
    - api
    - syntax
    - search
sidebar: "polyaxon-query-syntax"
---

Saved searches lets you save and describe search queries, for your groups, experiments, jobs, and builds. 
You can easily then monitor the results on an ongoing basis and find the desired results easily.
 
Saved Searches are important as well for comparing experiments, because it allows you to filter and reduce the number of experiments. 

Saved searches can be a way to monitor progress, specific changes, etc. 

We are also working on Alerts for saved searches so that you can be sent notified by email, Slack, or other integrations based on specific conditions,
ensuring you're aware of important things happening in your workflow.


## Examples of useful saved searches

### Recent finished experiments:

 * query: `status: succeeded | failed | stopped`
 * sort: `-finished_at`
 
### Best performing experiments based on a specific metrics:

 * query: `metric.loss: <=0.3, metric.precision: >=0.89`
 * sort: `metric.loss, -metric.precision`
 
### Experiment with specific code commit:

 * query: `commit: COMMIT-HASH`


## Creating saved searches

A saved search consist of a name (must be a slug) describing the search, and query/sort based on the specification.

Saved searches are created per project basis, only users having write access to the project can create a search, 
and they can be used by any user who has read access to the project, and so to the experiments, groups, builds, and jobs.  

To create a saved search, you need to create a query and / or a sort, and select the searches dropdown, 
and hit save. You will then have a chance to change the query/sort and provide a name for your search and save it.
