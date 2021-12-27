---
title: "VSCode"
meta_title: "VSCode"
meta_description: "Polyaxon makes it easy to start a VSCode session on your GPU cluster."
custom_excerpt: "Visual Studio Code is a free source-code editor made by Microsoft for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git."
image: "../../content/images/integrations/vscode.png"
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

Polyaxon makes it easy to start a VSCode session on your GPU cluster.

## Overview

Polyaxon schedules VSCode sessions based on this [component](https://cloud.polyaxon.com/ui/polyaxon/vscode/components/latest).

## Create a new session using the CLI

```bash
polyaxon run --hub vscode
```

To provide a specific tag:

```bash
polyaxon run --hub vscode:TAG_VERSION
```

To start the session on a different project

```bash
polyaxon run --hub vscode -p project-name
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

 * Light theme (Polyaxon and VSCode)

![vscode-service-light](../../content/images/integrations/vscode/vscode-service-light.png)

 * Dark theme (Polyaxon and VSCode)

![vscode-service-dark](../../content/images/integrations/vscode/vscode-service-dark.png)

## Queues, presets, node scheduling, custom resources, ... 

You can provide more information before scheduling the service, like the queue, presets, ...

```bash
polyaxon run --hub vscode -q agent-name/queue-name --presets preset-name1,preset-name2
```

Local preset

```bash
polyaxon run --hub vscode -f path/to/preset.yaml
```

You can also provide a full operation manifest to customize the environment section, node selector, connections, initializers, resources requirements, ...

```yaml
version: 1.1
kind: operation
hubRef: vscode
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

If you need to expose the `vscode` component with your predefined configuration without requiring end-users to create operations, 
we suggest that you clone the [component](https://cloud.polyaxon.com/ui/polyaxon/vscode/components/latest) and customize it.

On Polyaxon CE, you will need to create a new `.yaml` file where you will host the content of the component, and users can either start new sessions using:

 * `polyaxon run -f my-custom-vscode.yaml`
 * `polyaxon run --url https://path/to/my-custom-vscode.yaml` 

On Polyaxon Cloud or Polyaxon EE, you just need to add a new [component hub](/docs/management/component-hub/).
The end users will need to run with `org-name/vscode` instead of `vscode`:

```bash
polyaxon run --hub acme/vscode
```

> **Note**: In order to use `acme/vscode` without `:tag` you need to name the version `latest`.


## Versions

All `vscode` versions can be found on the [component hub](https://cloud.polyaxon.com/ui/polyaxon/vscode/components)

```bash
polyaxon hub ls -c vscode
```
