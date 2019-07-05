---
title: "Polyflow: Pipelines"
sub_link: "polyflow"
meta_title: "Polyaxon Polyflow: Pipelines - Polyaxon References Polyaxon"
meta_description: "Pipelines in Polyaxon are DAGs or a Directed Acyclic Graph – is a collection of all the operations you want to run, organized in a way that reflects their relationships and dependencies."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - polyflow
    - pipelines
    - dags
    - experimentation
sidebar: "polyflow"
---

> Polyflow is in beta, please reach out to us if you want to have early access

In Polyaflow, pipelines are DAGs or a Directed Acyclic Graph – a collection of all the operations you want to run, organized in a way that reflects their relationships and dependencies.

A pipeline's main goal is to describe and run several operations necessary for a Machine Learning (ML) workflow.

A pipeline execute a dependency graph of Kubernetes pods that execute the logic described in the template/action/event of that operation.

## Specification
 
 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: pipeline.
 * [logging](/references/polyaxonfile-yaml-specification/logging/): defines the logging.
 * tags: a list of strings.
 * backend: the backend for executing the pipeline.
 * [schedule](/references/polyflow/schedule/): defines if the pipeline should be executed in recurrent way following a cron definition or an interval definition.
 * concurrency: defines how many operations to schedule in parallel, if a pipeline define only sequential operation then this field has no effect.
 * ops `required`: the operations to run in the pipeline.
 * templates: the inline templates to use to resolve the ops definition in the pipeline. 

## Ops

Ops are the operations to run in the context of the pipeline, they can reference: 

 * inline templates
 * templates based on relative paths in the project
 * actions
 * events
 
### Specification

 * name: name of the operation
 * template: the template to use for this op.
     * Inline templates: `temaplate: {name: template-name}`
     * Path templates: `temaplate: {path: template-path}`
     * Actions: `temaplate: {action: action-name}`
     * Events: `temaplate: {event: event-name}`
 * params: parameters to resolve from other operations, it can be also raw values.
 * dependencies: name of all upstream operations, if params reference another op it will be added automatically to the dependencies, e.g. `[op1, op2]`  
 * trigger: `str` a policy to follow before triggering this op: `all_secceded`, `all_failed`, `all_done`, `one_succeeded`, `one_failed`, `one_done`
 * max_retries: `int` number of times to retry this operation after failing
 * retry_delay: `int`
 * retry_exp_backoff: `int`
 * max_retry_delay: `int`
 * skip_on_upstream_skip: `bool`

       
