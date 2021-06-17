---
title: "Context"
sub_link: "context"
meta_title: "Context - Polyaxon Specification"
meta_description: "Polyaxon provides a context to all runs to resolve information about params, id, project, ...."
visibility: public
status: published
is_index: true
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

Polyaxon provides a context used by Polyaxonfiles to resolve information about params, ids, project, ...

Users can use the `{{}}` to inject information that will be provided to the context when the operation is fully resolved.

Polyaxon uses [jinja](https://jinja.palletsprojects.com) to inject variables and params in the context and resolve the content defined inside `{{}}`, here are some useful links about [jinja](https://jinja.palletsprojects.com) that you can use in your Polyaxonfiles:
 * [Template](https://jinja.palletsprojects.com/en/3.0.x/templates)
 * [Builtin filters](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)
 * [Types examples](https://jinja.palletsprojects.com/en/3.0.x/nativetypes/#examples) 

## Compiler

Polyaxon uses a tool to compile the specification, every manifest that users submit to Polyaxon goes through several steps 
to ensure that the specification is correct and that is runnable. 

The compiler handles several use cases:
 * Sanitization
 * Type validation
 * Access validation
 * References resolution
 * Conversion

When used in the CLI or Client, the compiler will scan manifests and ensure that all required inputs and outputs have values and that all values are compatible with their types.
If a manifest has a DAG runtime, it will check that the graph is acyclic, that the information flowing from one operation to another is allowed and corresponds to the expected types.

The full compilation (resolution and conversion) is separated into two major steps, one on the control plane and the other on the agent running on the user's cluster, 
this way Polyaxon Control Plane does not require access to proprietary information or secrets and provides a federation layer.

In Polyaxon CE, this separation is nonexistent, and the compiler is very lightweight and runs on the API or the Scheduler.    

## Resolution 

The compiler is responsible for collecting and resolving variables.
It collects all variables and references coming from the inputs and outputs, connections schemas, presets, and metadata about runs.
If an operation is running in the context of a pipeline, DAG, Matrix, Mapping, ..., it will also collect information from the pipeline controller, the upstream and downstream runs.

If during the resolution, the compiler detects a missing reference or that the user initiating the operation does not have access to a specific resource, it will raise a compilation error.
After collecting all required information, it will start resolving the context and re-injecting additional information to be used in following steps.

## Context information

A resolved context will have several types of information collected during the compilation pipeline steps. 
It's very important to understand the order of these steps to build valid Polyaxonfiles.

### Global information

This is the information that is unique to each run.
Each run in Polyaxon has metadata about a project, an owner, and a user.
It has, as well, several metadata, e.g. time of creation, 
as well as specific information, e.g. component kind and runtime.

This information is available first and can be used immediately in all areas of the Polyaxonfile using the `{{ globals.* }}` prefix.

> **Note**: It's very important to note that when `globals.*` is used in a param section with `ref`, it will not correspond anymore to the current run, but will be resolved from the reference defined in the `param.ref`.

> **Note**: Please check the [context globals section](/docs/core/context/globals/) for more details.


### Params

This is the information coming from the params passed via CLI or one of the parameters' sections:
 * params
 * join params
 * matrix params

This information appears at the top level of the context and can be used without a prefix. 
However, you may need to access the meta-information about your inputs and outputs and not just the values, in which case you can use the `{{ params.* }}` prefix.

It's also possible to convert all params to a list of args: `{{ params.as_args }}` which is equivalent to `["--input1={{ input1 }}", "--input2={{ input2 }}", "--input3={{ input3 }}", ...]` or `["{{ params.input1.as_arg }}", "{{ params.input2.as_arg }}", "{{ params.input3.as_arg }}", ...]`.

Users can freely use any information from the `globals.*` section in params, 
since those values are already part of the context, and can be used if a param definition has a variable containing `globals.*`.

The params section is the most confusing section since parameters can come from several areas `params`, `matrix.params`, `joins.[JOIN].params`, 
and sometimes params might depend on each other before resolving the value.

It's very important to note the order when defining inputs and outputs.

Polyaxon goes through each input and resolves it, and adds any value to the context before moving forward to the next input.
This means that when creating an operation, the params section can define conditional values based on previous params, the order is the one defined in the inputs section.

When the compiler is done with the inputs, it moves to the outputs and performs a similar procedure. It's important to note that if both an input and an output have the same name, 
the context will only have one entry, if the output has a valid value, it will be the value used in the context.

After finishing the params section, the next section is the params defined in [joins](/docs/automation/joins/).
This implies that users can leverage information coming from `globals.*` and `params.*` (or as a shortcut `*`).
In general all values resolved in the joins params are lists, unless the values are defined using the [ArtifactsType](/docs/core/specification/types/#v1artifactstype), 
in which case the value is just a merged [ArtifactsType](/docs/core/specification/types/#v1artifactstype).

After resolving the joins, all resulting values will be available in the context, and the compiler moves to the last params section, params defined in the matrix section 
([Optimization](/docs/automation/optimization-engine/) or [Mapping](/docs/automation/mapping/)).

> **Note**: Please check the [context params section](/docs/core/context/params/) for more details.

### Connections

Finally, if the main container requests a connection or if an init container requests a connection, and if that connection has a schema, it will be available in the context.

> **Note**: Please check the [context connections section](/docs/core/context/connections/) for more details.

## Distributed jobs

If a Polyaxonfile defines a distributed job, each replica will receive a context with information from the `globals` level augmented with
information about the connections and init sections specific to each replica.
