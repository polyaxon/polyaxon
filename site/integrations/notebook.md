---
title: "Jupyter Notebook"
meta_title: "Jupyter Notebook"
meta_description: "Polyaxon makes it easy to start Jupyter Notebooks on your GPU cluster for you and your team members."
custom_excerpt: "The Jupyter Notebook is an incredibly powerful tool for interactively developing and presenting data science projects. A notebook integrates code and its output into a single document that combines visualizations, narrative text, mathematical equations, and other rich media."
image: "../../content/images/integrations/jupyter-notebook.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - services
  - experimentation
featured: false
popularity: 3
visibility: public
status: published
---

Polyaxon makes it easy to start a Jupyter Notebook session on your GPU cluster.

## Overview

Polyaxon schedules Jupyter Notebook sessions based on this [component](https://cloud.polyaxon.com/ui/polyaxon/notebook/components/latest).

## Create a new session using the CLI

```bash
polyaxon run --hub notebook
```

To provide a specific tag:

```bash
polyaxon run --hub notebook:TAG_VERSION
```

To start the session on a different project

```bash
polyaxon run --hub notebook -p project-name
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

![notebooks](../../content/images/concepts/dashboard/notebooks.png)


## Queues, presets, node scheduling, custom resources, ... 

You can provide more information before scheduling the service, like the queue, presets, ...

```bash
polyaxon run --hub notebook -q agent-name/queue-name --presets preset-name1,preset-name2
```

Local preset

```bash
polyaxon run --hub notebook -f path/to/preset.yaml
```

You can also provide a full operation manifest to customize the environment section, node selector, connections, initializers, resources requirements, ...

```yaml
version: 1.1
kind: operation
hubRef: notebook
runPatch:
  init:
    - git: ...
  connections: [...]
  environment:
    ...
  container:
    resources:
      requests:
        memory: 300Mi
``` 

## Forking and customizing the component

If you need to expose the `notebook` component with your predefined configuration without requiring end-users to create operations, 
we suggest that you clone the [component](https://cloud.polyaxon.com/ui/polyaxon/notebook/components/latest) and customize it.

On Polyaxon CE, you will need to create a new `.yaml` file where you will host the content of the component, and users can either start new sessions using:

 * `polyaxon run -f my-custom-notebook.yaml`
 * `polyaxon run --url https://path/to/my-custom-notebook.yaml` 

On Polyaxon Cloud or Polyaxon EE, you just need to add a new [component hub](/docs/management/component-hub/).
The end users will need to run with `org-name/notebook` instead of `notebook`:

```bash
polyaxon run --hub acme/notebook
```

> **Note**: In order to use `acme/notebook` without `:tag` you need to name the version `latest`.


## Versions

All `notebook` versions can be found on the [component hub](https://cloud.polyaxon.com/ui/polyaxon/notebook/components)

```bash
polyaxon hub ls -c notebook
```
