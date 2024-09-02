---
title: "Context Globals"
sub_link: "context/globals"
meta_title: "Context Globals - Polyaxon Specification"
meta_description: "This is the information that is unique to each run. Each run in Polyaxon has a project, an owner, and a user. It has as well several metadata like datetimes, e.g. time of creation, as well as information specific to the kind and runtime of the operation."
visibility: public
status: published
tags:
  - specification
  - api
  - polyaxon
  - yaml
  - json
  - python
sidebar: "core"
---

## Overview

`globals.*` is the section that defines the information that is unique to each run. Each run in Polyaxon has a project, an owner, and a user.
It has as well several metadata like datetimes, e.g. time of creation,
as well as information specific to the kind and runtime of the operation.

## Definition

Several variables are organized in the `globals.*` prefix,
this prevents information about a run to not conflict with the inputs and outputs you provide.

The following information can be accessed by all Polyaxon sections:

 * `{{ globals.owner_name }}`: The owner of the project where the run is saved.
 * `{{ globals.username }}`: The user who created the run (if available).
 * `{{ globals.project_name }}`: The project where the run is saved.
 * `{{ globals.project_unique_name }}`: Unique name of the project `owner.project_name`.
 * `{{ globals.project_uuid }}`: Project uuid.
 * `{{ globals.run_info }}`: `owner.project_name.uuid` unique name of the run.
 * `{{ globals.name }}`: The run name if available.
 * `{{ globals.uuid }}`: The run uuid.
 * `{{ globals.namespace }}`: The k8s namespace where the operation will be scheduled.
 * `{{ globals.context_path }}`: The context that Polyaxon will share with the main container: `/plx_context`. This context contains all artifacts and other configs.
 * `{{ globals.artifacts_path }}`: The artifacts root path that Polyaxon will share with the main container: `/plx_context/artifacts`, by default all connections will be populated under this path, unless the user sets a custom path.
 * `{{ globals.run_artifacts_path }}`: This the specific path where the run will store its artifacts, including those created and managed by Polyaxon `/plx_context/artifacts/run_uuid`.
 * `{{ globals.run_outputs_path }}`: Since the run artifacts will host artifacts and assets that are automatically created by Polyaxon, `/plx_context/artifacts/run_uuid/outputs` is a subpath that the user can use to store anything manually, like a tensorboard logs.
 * `{{ globals.created_at }}`: Datetime when the operation was created.
 * `{{ globals.compiled_at }}`: Datetime when the operation was compiled.
 * `{{ globals.cloning_kind }}`: Is populated if the operation is restarted or copied from another operation.
 * `{{ globals.original_uuid }}`: The original operation's uuid when the current operation was cloned from.
 * `{{ globals.is_independent }}`: A flag that tells id the operation is independent or part of a pipeline.
 * `{{ globals.iteration }}`: The iteration number if the operation is part of an iterative process.

## Artifacts store

If the artifacts store is requested via the `plugins.mount_artifacts_store` section, Polyaxon will expose the context variable `{{ globals.store_path }}` which is
the value of the volume path or the bucket url if the artifacts store is a blob storage.

## Services

If the Polyaxonfile contains a service runtime, the globals prefix will include additionally these information:

 * `{{ globals.base_url }}`
 * `{{ globals.ports }}`

## Schedules

When an operation is automatically created by a [schedule](/docs/automation/schedules/), the globals prefix will include additionally these information:

 * `{{ globals.schedule_at }}`: Datetime when the operation was supposed to be scheduled.

## Contexts and references

### Additional values

The context globals includes additional fields when used with a reference:

 * `{{ globals.status }}`: The last status of the reference operation.
 * `{{ globals.condition }}`: The last condition of the reference operation.
 * `{{ globals.finished_at }}`: The datetime when the operation finished.
 * `{{ globals.duration }}`: The duration of the operation.

### Usage

It's very important to note that when a param uses `globals.*`, it will depend on whether that param is literal or a reference, for example:

```yaml
params:
  param1:
    value: globals.uuid
  param2:
    ref: runs.UUID
    value: globals.uuid
  param3:
    ref: dag
    value: globals.uuid
  param4:
    ref: ops.upstream1
    value: globals.uuid
```

At first, you might think that all these params will have the same value, but that is not the case.

 * The value of `param1` will be the `uuid` of the run currently being compiled, meaning that each time you execute this Polyaxonfile, `param1` will take the `uuid` of that run.
 * The value of `param2` will be the `uuid` of the upstream run defined in the reference, ony if that run with `UUID` exists and is accessible to the current operation (mostly running in the same project).
   * this param is of course not necessary, since the `UUID` is already known to use it as a reference, but it could be any other value, for example `globals.started_at` which is a value that the user might not know at the time of creating the manifest.
 * If an operation is running in the context of a DAG, the value of `param3` will be the `uuid` of the pipeline managing the execution graph.
 * If an operation is running in the context of a DAG, the value of `param4` will be the `uuid` of the upstream operation that the current operation depends on.

> **Note**: For more details about references, please check [context references section](/docs/core/context/globals/) for more details.

## Distributed jobs

If your Polyaxonfile defines a distributed job, each replica will receive a context with information from the `globals` level augmented with
information about the connections and init sections specific to each replica.
