---
title: "Polyaxon Polyflow: Pipelines"
sub_link: "polyflow"
meta_title: "Polyaxon Polyflow: Pipelines - Polyaxon References Polyaxon"
meta_description: "Pipelines in Polyaxon are DAGs or a Directed Acyclic Graph – is a collection of all the operations you want to run, organized in a way that reflects their relationships and dependencies."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
sidebar: "polyflow"
---

> Polyflow is in beta, please reach out to us if you want to have early access

In Polyaxon, pipelines are DAGs or a Directed Acyclic Graph – a collection of all the operations you want to run, organized in a way that reflects their relationships and dependencies.

A pipeline's main goal is to describe and run several operations necessary for a Machine Learning(ML) workflow.

A pipeline execute a dependency graph of Kubernetes pods that execute the logic described in the template/action/event of that operation.

## Specification
 
 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: pipeline.
 * [logging](/references/polyaxonfile-yaml-specification/logging/): defines the logging.
 * tags: a list of strings.
 * backend: the backend for executing the pipeline.
 * schedule: defines if the pipeline should be executed in recurrent way following a cron definition or an interval definition.
 * concurrency: defines how many operations to schedule in parallel, if a pipeline define only sequential operation then this field has no effect.
 * ops `required`: the operations to run in the pipeline.
 * templates: the inline templates to use to resolve the ops definition in the pipeline. 


## Schedules

Polyaxon monitors all tasks and all DAGs, and triggers ops whose dependencies have been met. 

Pipeline are by default run one time, or as many times as the users trigger a new run.

To be able to trigger a pipeline repeatedly, a pipeline must define a schedule. Polyflow provides 2 ways to define a schedule to automate the process of creating pipeline runs.

### Interval schedules

A simple schedule is the interval schedule:

 * kind: interval
 * start_at: `optional`
 * end_at: `optional`
 * frequency: `required` / `str`
 * depends_on_past: `bool`


### Cron schedules

Cron schedule accepts a cron expression to create pipeline runs:

 * kind: cron
 * start_at: `optional`
 * end_at: `optional`
 * cron: `required` / `str`
 * depends_on_past: `bool`


## Ops

Ops are the operations to run in the context of the pipeline, they can reference: 

 * inline templates
 * templates based on relative paths in the project
 * actions
 * events
 
### Specification

 * name: name of the operation
 * template: the template to use for this op
 * params: parameters to resolve from other operations, it can be also raw values.
 * dependencies: name of all upstream operations, if params reference another op it will be added automatically to the dependencies.  
 * trigger: a policy to follow before triggering this op: ALL_SUCCEEDED, ALL_FAILED, ALL_DONE, ONE_SUCCEEDED, ONE_FAILED, ONE_DONE
 * max_retries: number of times to retry this operation after failing
 * retry_delay: `int`
 * retry_exp_backoff: `int`
 * max_retry_delay: `int`
 * skip_on_upstream_skip: `bool`

       
