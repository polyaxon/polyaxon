---
title: "RStudio"
meta_title: "RStudio"
meta_description: "Polyaxon makes it easy to start an RStudio session on your cluster."
custom_excerpt: "RStudio is an integrated development environment (IDE) for R, a programming language for statistical computing and graphics."
image: "../../content/images/integrations/rstudio.png"
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
popularity: 1
visibility: public
status: published
---

Polyaxon makes it easy to start an RStudio session on your cluster.

## Overview

Polyaxon schedules RStudio sessions based on this [component](https://cloud.polyaxon.com/ui/polyaxon/rstudio/components/latest).

## Create a new session using the CLI

```bash
polyaxon run --hub rstudio
```

To start a session with a specific theme:

```bash
polyaxon run --hub rstudio -P theme=Dracula
```

To start the session on a different project

```bash
polyaxon run --hub rstudio -p project-name
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

 * Light theme (Polyaxon and RStudio)

![rstudio-service-light](../../content/images/integrations/rstudio/rstudio-light.png)

 * Dark theme (Polyaxon and RStudio)

![rstudio-service-dark](../../content/images/integrations/rstudio/rstudio-dark.png)

## Queues, presets, node scheduling, custom resources, ... 

You can provide more information before scheduling the service, like the queue, presets, ...

```bash
polyaxon run --hub rstudio -q agent-name/queue-name --presets preset-name1,preset-name2
```

Local preset

```bash
polyaxon run --hub rstudio -f path/to/preset.yaml
```

You can also provide a full operation manifest to customize the environment section, node selector, connections, initializers, resources requirements, ...

```yaml
version: 1.1
kind: operation
hubRef: rstudio
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

If you need to expose the `rstudio` component with your predefined configuration without requiring end-users to create operations, 
we suggest that you clone the [component](https://cloud.polyaxon.com/ui/polyaxon/rstudio/components/latest) and customize it.

On Polyaxon CE, you will need to create a new `.yaml` file where you will host the content of the component, and users can either start new sessions using:

 * `polyaxon run -f my-custom-rstudio.yaml`
 * `polyaxon run --url https://path/to/my-custom-rstudio.yaml` 

On Polyaxon Cloud or Polyaxon EE, you just need to add a new [component hub](/docs/management/component-hub/).
The end users will need to run with `org-name/rstudio` instead of `rstudio`:

```bash
polyaxon run --hub acme/rstudio
```

> **Note**: In order to use `acme/rstudio` without `:tag` you need to name the version `latest`.


## Versions

All `rstudio` versions can be found on the [component hub](https://cloud.polyaxon.com/ui/polyaxon/rstudio/components)

```bash
polyaxon hub ls -c rstudio
```
