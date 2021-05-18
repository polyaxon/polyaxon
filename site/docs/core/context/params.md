---
title: "Context Params"
sub_link: "context/params"
meta_title: "Context Params - Polyaxon Specification"
meta_description: "Params Information is injected in the top level of the context and can be used without a prefix, additionally Polyaxon exposes a prefix params to provide extra information about the params context."
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

Params provide values to the inputs and outputs definition, and can provide context only values as well.
The information provided in the params is injected after the [globals context information](/docs/core/context/globals/), which can be accessed without prefix or using the `params.*` prefix.   

## Top level access

The values of the inputs and the outputs are made available in the top level of the context, this means that when users are developing their Polyaxonfiles,
they can use the variables defined in their inputs and outputs without any prefix:

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

## Getting all params

The params prefix allows to convert all params to a list of arguments:

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
    args: "{{ params.as_args }}"
```

## Params prefix

Sometimes users will need to access the meta-information about their inputs and outputs and not just the values, 
for instance let take the following example, a component that returns a docker image:

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

And this is an example of an operation to use with this component:

```yaml
version: 1.1
kind: component
name: build
params:
  destination:
    connection: docker-connection
    value: "image:tag"
...
```

This component is using the params to pass the destination value as well as a connection that will be used to authenticate the registry, 
both the parameter's value and connection are used in this component:

`{{ destination }}` is only a shortcut for exposing inputs/outputs params' values which also exists on the `params` prefix, e.g. `{{ params.destination.value }}`.
The `params.*` prefix exposes several other information if the user needs to access metadata and not just the value, 
these are all the information exposed under the `params` prefix for each input/output:

 * `{{params.param-name.value}}`: The value that will be checked against the IO type.
 * `{{params.param-name.connection}}`: A connection that is passed with the param.
 * `{{params.param-name.as_arg}}`: A string representing an argument representation of the param's value, this only get injected if the value is not null, i.e. `--param-name={{ value }}` or `--param-name` if the value is of type boolean.
 * `{{params.param-name.as_str}}`: A string representing of the param's value.
 * `{{params.param-name.type}}`: The type of the param based on the Input/Output configuration.

## Params resolution order

It's very important to understand how Polyaxon resolves params to build valid Polyaxonfiles.

Polyaxon resolves params in this order:

 1. top level params section.
 3. join params section.
 2. matrix params sections.

Le's see the impact of this order with some examples.

### Using params in joins

Let's see first how we can use globals in joins:

```yaml
kind: operation
...
joins:
- query: "metrics.loss:<0.1, project.name:{{ globals.project_name }}"
  sort: "metrics.loss"
  params:
    tensorboards: {value: "artifacts.tensorboard", contextOnly: true}
```

In this example we are using the `project_name` which is resolved from the current run, 
to filter for all runs that we will request the tensorboard path from. (`artifacts.tensorboard` requests the lineage information if reported.) 

If we decide to template the max loss or to limit the number of runs to fetch the tensorboard path from, we can do the following:


```yaml
kind: operation
...
joins:
- query: "metrics.loss:<{{ max_loss }}, project.name:{{ globals.project_name }}"
  sort: "metrics.loss"
  limit: "{{ limit }}"
  params:
    tensorboards: {value: "artifacts.tensorboard", contextOnly: true}
params:
  max_loss:
    value: 0.1
    contextOnly: True
  limit:
    value: 5
    contextOnly: True
```

This is not different from setting the values directly, but sometimes you may need to use a variable several times without using magic strings.

To take this to the next level, the params can come from an input definition:

```yaml
kind: operation
...
joins:
- query: "metrics.loss:<{{ max_loss }}, project.name:{{ globals.project_name }}"
  sort: "metrics.loss"
  limit: "{{ limit }}"
  params:
    tensorboards: {value: "artifacts.tensorboard", contextOnly: true}
component:
  inputs:
  - {name: limit, type: int, value: 5, isOptional: true, description: "top experiments."}
  - {name: max_loss, type: float, value: 0.01, isOptional: true, description: "maximum loss."}
```

Another use case is running a map reduce style DAG, in which case you may need to filter for operation coming from an upstream matrix:

```yaml
version: 1.1
kind: component
inputs:
- {name: limit, type: int, value: 5, isOptional: true, description: "top experiments."}
- {name: min_accuracy, type: float, value: 0.9, isOptional: true, description: "min accuracy."}
run:
  kind: dag
  operations:
  - name: tune
    dagRef: ...
    matrix:
      kind: random
      concurrency: 5
      numRuns: 20
      params:
        learning_rate:
          kind: linspace
          value: 0.001:0.1:5
        dropout:
          kind: choice
          value: [0.25, 0.3]
        conv_activation:
          kind: pchoice
          value: [[relu, 0.1], [sigmoid, 0.8]]
        epochs:
          kind: choice
          value: [5, 10]
  - name: best_models
    dagRef: ...
    joins:
    - query: "metrics.accuracy:>{{ min_accuracy }}, project.name:{{ tune_uuid }}, kind: job"
      sort: "-metrics.accuracy"
      limit: "{{ limit }}"
      params:
        uuids: {value: "globals.uuid", contextOnly: true}
        learning_rates: {value: "inputs.learning_rate", contextOnly: true}
        accuracies: {value: "outputs.accuracy", contextOnly: true}
        losses: {value: "outputs.loss", contextOnly: true}
    params:
      limit:
        ref: dag
        value: inputs.limit
        contextOnly: true
      max_loss:
        ref: dag
        value: inputs.max_loss
        contextOnly: true
      tune_uuid:
        ref: ops.tune
        value: globals.uuid
        contextOnly: true
```

This is a more complex example, but we will try to explain how information is passed from the DAG and from the operation to the last operation with joins. 

 * We declare a component with a DAG runtime. This component has 2 optional inputs.
 * This dag has also two operations: one operation for running hyperparameter tuning followed by an operation that fetches the top experiments based on their accuracies.
 * To restrict the `best_models` operation to only look for runs in the `tune` operation, we are requesting first the uuid as a `contextOnly` which allows us to declare 
 that param and instruct Polyaxon to not validate it against the IO declaration.
 * We are also restricting the `best_models` operation to only look for operations with an accuracy higher than the parameter passed to our DAG, with a default equal to 0.9.
 * Finally, we are only interested in 5 runs or any number we decide to pass to the DAG with the limit input. Again, we use the param with `ref: dag` to request those values and make them available to the operation.
 * In the end we see that the join itself is exposing several params: the `uuids` of all runs found, their `learning_rates` their `accuracies`, and their `losses`.


Note that we are using `contextOnly` for all the params defined in the join. 
If the definition of the component `dagRef` for the `best_models` operation is expecting inputs and outputs, 
`contextOnly` would not be necessary, and those values will be validated. An example of a such component would have the following IO definition:

```yaml
inputs:
- {name: uuids, type: uuid, isList: true}
- {name: learning_rates, type: float, isList: true}
- {name: accuracies, type: float, isList: true}
- {name: losses, type: float, isList: true}
``` 

It's important to use `isList: true` otherwise, the compiler will raise an error because the join is returning a list and the user is expecting a single value.


### Using params and joins in matrix

Similarly, since `matrix.params` are the last to be resolved, you can use any param from the main params section or the joins section in your matrix definition.

```yaml
matrix:
  kind: random
  concurrency: 5
  numRuns: 20
  params:
    some_choice_param:
      kind: choice
      value: {{ param_choice }}
params:
  param_choice:
    value: [foo, bar]
    contextOnly: true
```

A similar analysis can be applied here as well, the `param_choice` value can be coming either from an upstream operation or as a dynamic input. 
