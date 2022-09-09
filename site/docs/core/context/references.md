---
title: "Context References"
sub_link: "context/references"
meta_title: "Context References - Polyaxon Specification"
meta_description: "Params can be resolved based on literal values or can be resolved based on a reference."
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

Param values can be resolved based on literal values or can be resolved based on a reference.
When a reference is used, it is important to not be confused about the source of the information.

When a reference is created, Polyaxon will automatically collect a lineage information and expose it in the lineage table under upstream/downstream tabs.

## Definition

Anytime a param is using the `ref` key, users should be aware that the `value` key is not pointing to the current run's context anymore, rather,
it's requesting information from the reference.

For example:

```yaml
params:
  param_upstream_op_uuid:
    ref: ops.upstream1
    value: globals.uuid
  param_upstream_op_input:
    ref: ops.upstream1
    value: inputs.in_name_foo
```

or from a pipeline:


```yaml
params:
  param_dag_uuid:
    ref: dag
    value: globals.uuid
  param_dag_input:
    ref: dag
    value: inputs.in_name_foo
```

The following `param_foo` is not going to use the current run `globals.*` instead it will use whatever run instance of the upstream operation, 
which means that every time a dag is executed there will new runs with new uuids, one for the current run and one for the upstream run, `param_foo` will be pointing to the upstream run.

this is the only way to use `globals.*` of the upstream run without clashing with the default `globals.uuid` of the current run. 
We made the decision to force an explicit request of any reference that does not belong to the current context via a parameter.

## References

Each parameter can use the following references:

 * `ref: runs.UUID`: if you need to request an information from some previous run and delegate the logic of fetching those values to Polyaxon to be performed automatically. 
 * `ref: dag`: if defined in the context of a DAG, and you need to request some information from the pipeline that manages the DAG.
 * `ref: ops.NAME`: if defined in the context of a DAG, and you need to request some information from an upstream operation.
 
## Values

Each parameter with `ref` can request the following information that reference:

 * `globals`: All general context information from the reference as a dictionary.
 * `globals.*`: Specific general context value from the reference.
 * `io`: All Inputs/outputs/artifacts information from the reference as a dictionary `{"inputs": {}, "outputs": {}, "artifacts": {}}`.
 * `inputs`: All inputs (key -> value) from the reference as a dictionary.
 * `inputs.*`: Specific input value from the reference.
 * `outputs`: All outputs (key -> value) from the reference as a dictionary.
 * `outputs.*`: Specific output value from the reference.
 * `artifacts`: All artifacts lineage paths as a dictionary.
 * `artifacts.base`: The base path of the run, basically the path defined by `uuid`.
 * `artifacts.outputs`: The base outputs path of the run, basically the path defined by `uuid/outputs`.
 * `artifacts.*`: Specific path coming logged in the lineage table, e.g. `artifacts.tensorboard`.
 * `{"file": [..., ...], "dirs": [..., ...]}`: An [ArtifactsType](/docs/core/specification/types/#v1artifactstype) definition, and it can be used with `toInit` or can be passed to the `init` section. 
 

## Exceptions

It's important to note that you cannot provide `ref` to joins' params or matrix params.
Each join constructs the references based on the query/sort/limit/offset specification.
