---
title: "JupyterLab"
meta_title: "JupyterLab"
meta_description: "Polyaxon makes it easy to start JupyterLab on your GPU cluster for you and your team members."
custom_excerpt: "JupyterLab is an extensible environment for interactive and reproducible computing, based on the Jupyter Notebook and Architecture."
image: "../../content/images/integrations/jupyter-lab.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - services
  - experimentation
featured: true
popularity: 3
visibility: public
status: published
---

Polyaxon makes it easy to start a JupyterLab session on your GPU cluster.

## Overview

Polyaxon schedules JupyterLab sessions based on this [component](https://cloud.polyaxon.com/ui/polyaxon/jupyterlab/components/latest).

## Create a new session using the CLI

```bash
polyaxon run --hub jupyterlab
```

To provide a specific tag:

```bash
polyaxon run --hub jupyterlab:TAG_VERSION
```

To start the session on a different project

```bash
polyaxon run --hub jupyterlab -p project-name
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

![jupyter-lab](../../content/images/dashboard/runs/notebook-explore-models.png)


## Queues, presets, node scheduling, custom resources, ... 

You can provide more information before scheduling the service, like the queue, presets, ...

```bash
polyaxon run --hub jupyterlab -q agent-name/queue-name --presets preset-name1,preset-name2
```

Local preset

```bash
polyaxon run --hub jupyterlab -f path/to/preset.yaml
```

You can also provide a full operation manifest to customize the environment section, node selector, connections, initializers, resources requirements, ...

```yaml
version: 1.1
kind: operation
hubRef: jupyterlab
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

If you need to expose the `jupyterlab` component with your predefined configuration without requiring end-users to create operations, 
we suggest that you clone the [component](https://cloud.polyaxon.com/ui/polyaxon/jupyterlab/components/latest) and customize it.

On Polyaxon CE, you will need to create a new `.yaml` file where you will host the content of the component, and users can either start new sessions using:

 * `polyaxon run -f my-custom-jupyterlab.yaml`
 * `polyaxon run --url https://path/to/my-custom-jupyterlab.yaml` 

On Polyaxon Cloud or Polyaxon EE, you just need to add a new [component hub](/docs/management/component-hub/).
The end users will need to run with `org-name/jupyterlab` instead of `jupyterlab`:

```bash
polyaxon run --hub acme/jupyterlab
```

> **Note**: In order to use `acme/jupyterlab` without `:tag` you need to name the version `latest`.


## Versions

All `jupyterlab` versions can be found on the [component hub](https://cloud.polyaxon.com/ui/polyaxon/jupyterlab/components)

```bash
polyaxon hub ls -c jupyterlab
```
