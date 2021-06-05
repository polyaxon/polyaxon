---
title: "Services Timeout"
sub_link: "scheduling-presets/services-timeout"
meta_title: "Services Timeout - scheduling presets"
meta_description: "Cleaning Jupyter notebooks and Tensorboard session automatically with a timeout preset."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

Polyaxon provides a simple process for spawning and managing Jupyter notebooks, Tensorboard, RStudio, and other services.
Oftentimes, users will start a Tensorboard session or notebook server that requests GPU resources and will forget stopping the service.

As an admin you can create, or even enforce a timeout mechanism, on these type of services using a preset.    

## Defining a timeout preset

Defining a timeout preset is straightforward in Polyaxon:

```yaml
termination:
  timeout: 86400 # 24 hours 
```  

By [saving this preset](/docs/management/organizations/presets/) as `services-timeout-24`,
users can automatically clean their sessions after 24 hours:

```bash
polyaxon run ... --presets=services-timeout-24
```

You can also use the preset directly on the component or operation definition:

```yaml
kind: operation
presets: [services-timeout-24]
...
```
