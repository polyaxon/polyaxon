---
title: "Quick Start: Operations"
sub_link: "quick-start/operations"
meta_title: "Operations - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Operations - Get started with Polyaxon and become familiar with the ecosystem of Polyaxon with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - quick-start
sidebar: "core"
---

In the previous section we looked at components, we also saw how to create components with inputs/outputs
to run our model with different parameters without changing the code or the component itself.

In this sections we will look at what happened when we run a component w/o params.

## Understanding the process

Let's first run this polyaxonfile:

```bash
$ polyaxon run --url=https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/operation.yml
```

> For more details about this command please run `polyaxon run --help`,
or check the [command reference](/docs/core/cli/run/)

This file `operation.yml` also creates a new run, but its content does not include a component, it includes an operation.

```yaml
version: 1.1
kind: operation
params:
  optimizer: {value: sgd}
  epochs: {value: 1}
urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yml
```

An operation just defines how to run a component, running this file does not require passing params using the CLI because they are defined in the polyaxonfile.

## The run command

When a user runs the command `polyaxon run`, Polyaxon checks if the file contains a component or an operation:
 * If it contains a component it will create an operation based on the params passed, the name, description, tags, queue, profile if provided.
 * If the file contains an operation, then it checks if it can be executed.

But why create a file when we can just run the command with parameters and some flags?
Creating a file with an operation allows to define more complex executables for our components,
for instance if we want to run the same component with GPU, we have 2 options:
 * We can parametrize the resource section and Add inputs to define the number of GPUs. This not ideal because the number of inputs will grow fast every time we need to pass an information.
 * Use an operation to patch the component with all information required to run it in the environment of our choice without changing the component itself.

```yaml
version: 1.1
kind: operation
params:
  optimizer: {value: sgd}
  epochs: {value: 1}
runPatch:
  container:
    resources:
      limits:
        nvidia.com/gpu: 1
urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yml
```

Using the operation we will keep the options to use other resources or no resources at all, you can also patch the environment, init, sidecars ...

Sometime you might want to create a component with predefined values or sometimes the values might not need to change often,
in that case it will make sense to push more information to the component.

## Referencing a component

Since operations don't define a runtime, they need to reference components to run.

Operations can reference components in several ways:

 * `urlRef`: This is what we used earlier to resolve the component to run, basically Polyaxon will fetch the content of the component based on a url.
 * `pathRef`: If we were to clone the repo we could replace the `urlRef` with a simple `pathRef: ./typed.yml` since both files are on the same folder.
 * `hubRef`: This is similar to what we did for running Tensorboard with the `--hub` argument, in fact the CLI just injects this option using that flag.
 * `component`: It's possible to pass the component inline directly inside the operation, this use case is generally useful when running DAGs.

## Conclusion

Operations are how you execute components. To learn more about operations, please check the [specification section](/docs/core/specification/operation/)

The next section of [this tutorial](/docs/core/quick-start/iterate/) we will explore how to use notebooks to run an interactive process for scheduling experiments.
