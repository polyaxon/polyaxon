---
title: "Organizing Workload"
sub_link: "scheduling-presets/organizing-workload"
meta_title: "Organizing Workload - scheduling presets"
meta_description: "Most teams will need to assign different workload to different machines."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

Most teams will need to assign different workload to different machines, some of this workload has a very clear profile like builds, Tensorboard, ...
As an admin you can create several workload profiles using presets to simplify the process of assigning pods to nodes.    

## Defining a workload profile

Defining a workload profile using a presets can be as simple as setting a default node selector or as complex as defining a [catalog of machines](/docs/core/scheduling-presets/machines-catalog/).

 * Builds

```yaml
runPatch:
  environment:
    nodeName: build-node
```  

You can [save this preset](/docs/management/organizations/presets/) as `build-node`.

 * Experiments

```yaml
runPatch:
  environment:
    nodeSelector:
      polyaxon: experiments
```  

You can [save this preset](/docs/management/organizations/presets/) as `default-experiments-selector`.
