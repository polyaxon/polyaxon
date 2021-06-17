---
title: "Estimating Cost"
sub_link: "scheduling-strategies/estimating-cost"
meta_title: "Estimating Cost - scheduling strategies"
meta_description: "Define cost per operation or environment."
visibility: public
status: published
tags:
  - tutorials
  - concepts
sidebar: "core"
---

## Overview

Polyaxon provides a feature to set a cost estimation per operation:
 * The cost can map directly to the cost of a cloud instance or a complex definition/convention for running an operation type 
 * The cost can be set directly on the component or the operation level, but it can also be set directly on the presets, especially when defining a [catalog of environments](/docs/core/scheduling-presets/machines-catalog/).

Whe you define a cost estimation, Polyaxon will allow you to:
 * Filter runs by their cost estimation
 * Calculate cost estimation by project
 * Generate cost analytics per user, team, project, queue, agent
 * Communicate cost estimation to customers or to managers
  
## Setting the cost on the components

You can define the cost directly on the component to enable cost estimation:

```yaml
version: ...
kind: component
cost: 300
...
```

Defining cost on the component could be useful when the component is defined in the component hub, when it rarely changes, and it always runs on the same environment, e.g. build jobs.

## Setting the cost on presets

When you organize a catalog of environments or machines using presets you can also define the cost directly on the presets, for instance, 
if you provide two build environments, one with a small instance and one with a large instance, setting the cost directly on the component 
does not make sense, instead the cost should be directly attached to the environment where it's running:

Small build node

```yaml
cost: 0.0008
runPatch:
  environment:
    nodeName: small-build-node
  container:
    resources:
      requests:
        cpu: "500m"
```  

Large build node

```yaml
cost: 0.016
runPatch:
  environment:
    nodeName: large-build-node
  container:
    resources:
      requests:
        cpu: "8"
```  

