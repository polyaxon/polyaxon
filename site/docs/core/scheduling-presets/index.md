---
title: "Scheduling Presets"
sub_link: "scheduling-presets"
meta_title: "Presets allows to define configurations that should be injected into operation at compilation time - scheduling presets"
meta_description: "A feature for injecting certain information into operations at compilation time to extract repetitive configuration for node scheduling, resources requirements and definition, connections, 
but also for queue routing and access level control."
is_index: true
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

Scheduling presets is a feature for injecting certain information into operations at compilation time to extract repetitive configuration for node scheduling, resources requirements and definition, connections, 
but also for queue routing and access level control.

## Why using a preset

It's possible to set for each operation an
[environment section](/docs/core/specification/environment/), a [queue](/docs/core/specification/operation/#queue), a [container resources requirements](https://kubernetes.io/docs/concepts/containers/),
a [termination](/docs/core/specification/termination/). But oftentimes, you might want to reuse some or all of these options
and apply them to a certain type of operations.

One way to achieve such workflow is to push as many configuration sections as possible to the components, but this is not always possible and it's not recommended,
either because a component should be generic or because the component should be used across different clusters, with different references for queues, nodes, ...

Polyaxon provides a concept called `Presets`, that you can use to package several information about how to predefine your operations.

## Defining presets

Presets use all sections that the [operation specification](/docs/core/specification/operation/) offers, except for sections that define the component runtime, i.e.:
 * hubRef
 * dagRef
 * urlRef
 * pathRef
 * component

Each preset that you define can also have a `patchStrategy` that defines how the preset specification will be merged with main operation that you desire to run.
Polyaxon exposes four patch strategies:

 * `replace`: replaces all keys with new values if provided.
 * `isnull`: only applies new values if the keys have empty/None values.
 * `post_merge`: applies deep merge where newer values are applied last.
 * `pre_merge`: applies deep merge where newer values are applied first.

## Saving presets

There are two ways to define and save presets:

 * In your git projects using Polyaxonfiles.
 * In your Polyaxon organization using the UI (Polyaxon **EE** and **Cloud**).

### Presets using Polyaxonfiles

You can define a preset similar to any other Polyaxonfile that contain an operation.
Presets can help define scheduling and environment configurations that you can share with 
the rest of your team to reduce the amount of boilerplate in your main Polyaxonfiles. Let's look at some example of presets.

 * **Preset for node scheduling**

In order to leverage several node groups that can be used for scheduling your operations you can create several presets, 
e.g. `experiments.yaml`, `gpu_experiments.yaml`, `data_loaders.yaml`, `build_jobs.yaml` instead of setting an `environment` section on each component or operation.
Each one of these files can define the node labels, annotations, tolerations and affinities,

For example The `gpu_experiments.yaml` can contain the following specification:

```yaml
runPatch:
  environment:
    nodeSelector:
      node_label: gpu-experiments
```
 
you can commit these files with your git projects, and other users in your cluster don't have to learn how to request GPUs in their jobs or go through the same steps to define the environment section,
they can just use the override argument:

```bash
polyaxon run -f main.yaml -f presets/gpu_experiments.yaml
```
or
```bash
polyaxon run --hub COMPONENT_NAME -f presets/gpu_experiments.yaml
```
or
```bash
polyaxon run --url ... -f presets/gpu_experiments.yaml
```

Polyaxon will extend the main operation with all sections defined in `gpu_experiments.yaml` following the `patchStrategy` if defined in the preset otherwise use the default `replace` patch strategy.

Note that `isPreset: true` is optional, anything that comes after the main component/operation using the override argument `-f` will be considered a preset even if it does not contain the `isPreset` flag.

 * **Preset for defining resources requirements**
 
You can also define presets to extract information about resources requirements, for example you might define `small_instance.yaml`, `medium_instance.yaml`, and `large_instance.yaml`.
The content of these presets can contain information about resources requests and limits, for instance the `large_instance.yaml`

```yaml
patchStrategy: isnull
runPatch:
  container:
    resources:
      limits:
        nvidia.com/gpu: 4
```

You can also use one or more presets:

```bash
polyaxon run -f main.yaml -f presets/gpu_experiments.yaml -f presets/large_instance.yaml
```
or
```bash
polyaxon run --hub COMPONENT_NAME -f presets/gpu_experiments.yaml -f presets/large_instance.yaml
```
or
```bash
polyaxon run --url ... -f presets/gpu_experiments.yaml -f presets/large_instance.yaml
```

Polyaxon will follow the order of these presets and will patch the main operation/component following the `patchStrategy` defined in each one of these presets.

### Organization level saved presets

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

If you have access to Polyaxon Cloud or Polyaxon EE you can also save these presets on the organization level.
You can additionally set the default preset on your organization or on a project level using Polyaxon UI, 
such preset will be applied to all operations in the organization or the project where it's set.    

Users can just reference the presets in their [operations specification](/docs/core/specification/operation/#presets) or using the CLI/Client `polyaxon run ... --presets=preset1,preset2`

In order to create and manage scheduling presets, please check the [management section for more details](/docs/management/organizations/presets/)
