---
title: "Tensorboard"
meta_title: "Tensorboard"
meta_description: "Polyaxon integrates with Tensorboard to visualize and debug deep learning models. Polyaxon provides several ways for using Tensorboard."
custom_excerpt: "TensorBoard provides the visualization and tooling needed for machine learning experimentation: Tracking and visualizing metrics such as loss and accuracy Visualizing the model graph (ops and layers)."
image: "../../content/images/integrations/tensorflow.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - services
  - dashboard
featured: true
popularity: 3
visibility: public
status: published
---

Polyaxon integrates with Tensorboard to visualize and debug deep learning models.

## Overview

Polyaxon provides several ways for using Tensorboard, you can check the [component on Polyaxon](https://cloud.polyaxon.com/ui/polyaxon/tensorboard/components) for more details.

> **Note**: The default version `latest` targets a single run, and it has the same component's content as `tensorboard:single-run`. 

## Create a new tensorboard using the CLI

```bash
polyaxon run --hub tensorboard -P uuid=UUID
```

The `UUID` is the uuid of the experiment to start a tensorboard for.

To provide a specific tag:

```bash
 polyaxon run --hub tensorboard:multi-run -P uuids=UUID1,UUID2
```

To start the session on a different project

```bash
polyaxon run --hub tensorboard -p project-name
```


## Viewing the service 

Go to the UI under the `service` tab:

```bash
polyaxon ops dashboard [-uid] [-p]
```

Or to get to the service directly:

```bash
polyaxon ops service [-uid] [-p]
```

Or to get the service in full-screen mode:

```bash
polyaxon ops service --external [-uid] [-p]
```

 * Single-run tensorboard

![run-dashboards-tensorboard](../../content/images/dashboard/runs/dashboards-tensorboard.png)

![run-dashboards-tensorboard-histo](../../content/images/dashboard/runs/dashboards-tensorboard-histo.png)

 * Multi-run tensorboard

![run-dashboards-tensorboard](../../content/images/dashboard/comparison/tensorboard.png)

![comparison-tensorboard-compare](../../content/images/dashboard/comparison/tensorboard-compare.png)


## Queues, presets, node scheduling, custom resources, ... 

You can provide more information before scheduling the service, like the queue, presets, ...

```bash
polyaxon run --hub tensorboard -q agent-name/queue-name --presets preset-name1,preset-name2
```

Local preset

```bash
polyaxon run --hub tensorboard -f path/to/preset.yaml
```

You can also provide a full operation manifest to customize the environment section, node selector, connections, initializers, resources requirements, ...

```yaml
version: 1.1
kind: operation
hubRef: tensorboard
runPatch:
  connections: [...]
  environment:
    ...
  container:
    resources:
      requests:
        memory: 300Mi
``` 

## Forking and customizing the component

If you need to expose the `tensorboard` component with your predefined configuration without requiring end-users to create operations, 
we suggest that you clone the [component](https://cloud.polyaxon.com/ui/polyaxon/tensorboard/components/latest) and customize it.

On Polyaxon CE, you will need to create a new `.yaml` file where you will host the content of the component, and users can either start new sessions using:

 * `polyaxon run -f my-custom-tensorboard.yaml`
 * `polyaxon run --url https://path/to/my-custom-tensorboard.yaml` 

On Polyaxon Cloud or Polyaxon EE, you just need to add a new [component hub](/docs/management/component-hub/).
The end users will need to run with `org-name/tensorboard` instead of `tensorboard`:

```bash
polyaxon run --hub acme/tensorboard
```

> **Note**: In order to use `acme/tensorboard` without `:tag` you need to name the version `latest`.


## Versions

All `tensorboard` versions can be found on the [component hub](https://cloud.polyaxon.com/ui/polyaxon/tensorboard/components)

```bash
polyaxon hub ls -c tensorboard
```
