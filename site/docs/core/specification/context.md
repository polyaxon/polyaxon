---
title: "Context Specification"
sub_link: "specification/context"
meta_title: "Context - Polyaxon Specification"
meta_description: "Polyaxon provides a context to all runs to resolve information about params, id, project, ...."
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

Polyaxon provides a context to all runs to resolve information about params, id, project, ....

Users can use the `{{}}` to inject information that will be provided to the context when the operation is fully resolved.

## Top level information

Information in the top level of a context can be used without a prefix.
The values of the inputs and the outputs are set on the top level, this means that when you are developing your components,
you can use the variables defined in your inputs and outputs without any prefix:

```yaml
version: 1.1
kind: component
inputs:
- name: intput1
  type: str
- name: input2
  type: str

run:
  kind: job
  container:
    image: "image:test"
    command: ["command"]
    args: [
      "--param1={{input1}}",
      "--param2={{input2}}",
    ]
```

## Params

Sometimes you need to access the meta=information about your inputs and outputs and not just the values, 
for instance let take the example of a component that outputs a docker image:

```yaml
version: 1.1
kind: component

outputs:
- name: destination
  type: image

run:
  kind: job
  connections: ["{{ params.destination.connection }}"]
  container:
    image: "image:test"
    command: ["command"]
    args: [{{connections[params.destination.connection].url + '/' + destination}}]
```

this is an example of an operation to use with this component:

```yaml
version: 1.1
kind: component
name: build
params:
  destination:
    connection: docker-connection
    value: polyaxon-quick-start:dev
...
```

This component is using the params to pass the destination value as well as a connection that will be used to authenticate the registry, 
both the parameter' value and connection are used in this component:

`{{ destination }}` is only a shortcut for exposing inputs/outputs params' values which also exists on the `params` prefix, e.g. `{{ params.destination.value }}`.
The `params` prefix exposes several other information if the user needs to access metadata and not just the value, these are all the information exposed under the `params` prefix for each input/output:

 * `{{params.param-name.value}}`: The value that will be checked against the IO type.
 * `{{params.param-name.connection}}`: A connection that is passed with the param.
 * `{{params.param-name.as_arg}}`: A string representing an argument representation of the param's value, this only get injected if the value is not null, i.e. `--param-name={{ value }}` or `--param-name` if the value is of type boolean.
 * `{{params.param-name.as_str}}`: A string representing of the param's value.
 * `{{params.param-name.type}}`: The type of the param based on the Input/Output configuration.


## Globals

Several information is organized in a `globals` prefix,
this prevents information about a run to not conflict with the inputs and outputs you provide.

The following information can be accessed by all Polyaxon components:

 * `{{ globals.owner_name }}`: The owner of the project where the run is saved.
 * `{{ globals.project_name }}`: The project where the run is saved.
 * `{{ globals.project_unique_name }}`: Unique name of the project `owner.project_name`.
 * `{{ globals.project_uuid }}`: Project uuid.
 * `{{ globals.run_info }}`: `owner.project_name.uuid` unique name of the run.
 * `{{ globals.name }}`: The run name if available.
 * `{{ globals.uuid }}`: The run uuid.
 * `{{ globals.namespace }}`: The k8s namespace where the operation will be scheduled.
 * `{{ globals.context_path }}`: The context that Polyaxon will share with the main container: `/plx_context`. This context contains all artifacts and other configs.
 * `{{ globals.artifacts_path }}`: The artifacts root path that Polyaxon will share with the main container: `/plx_context/artifacts`, by default all connections will be populated under this path, unless the user sets a custom path.
 * `{{ globals.run_artifacts_path }}`: This where this specific run will store its artifacts, including those created and managed by Polyaxon `/plx_context/artifacts/run_uuid`.
 * `{{ globals.run_outputs_path }}`: Since the run artifacts will host artifacts and assets that are automatically created by Polyaxon, `/plx_context/artifacts/run_uuid/outputs` is a subpath that the user can use to store anything manually.
 * `{{ globals.created_at }}`: Datetime when the operation was created.
 * `{{ globals.compiled_at }}`: Datetime when the operation was compiled.
 * `{{ globals.cloning_kind }}`: Is populated if the operation is restarted or copied from another operation.
 * `{{ globals.original_uuid }}`: The original operation's uuid when the current operation was cloned from.
 * `{{ globals.iteration }}`

## Services

If you are authoring a component that contains a service, the globals prefix will include additionally these information:

 * `{{ globals.base_url }}`
 * `{{ globals.ports }}`

## Connections

Similarly, if you add a connection or an init container that requests a connection, if that connection has any schema, it will be available in the context:

> Several connections do not have a schema, and just expose env vars or mount secret volumes

```yaml
version: 1.1
kind: component
inputs:
- name: intput1
  type: str
- name: input2
  type: str

run:
  kind: job
  init:
  - connection: connection-with-schema
    container:
      image: "custom-container"
      command: ["echo"]
      args: ["{{ init[connection-with-schema].schemaKey }}"]
  connections: ["some-git-connection"]
  container:
    image: "image:test"
    command: ["command"]
    args: [
      "--param1={{ input1 }}",
      "--param2={{ input2 }}",
      "--param3={{ connections[some-git-connection].url }}"
    ]
```

## Distributed jobs

If your Polyaxonfile defines a distributed job, each replica will receive a context with information from the `globals` level augmented with
information about the connections and init sections specific to each replica.
