---
title: "Run Profiles"
sub_link: "scheduling-strategies/run-profiles"
meta_title: "Preset with Run profiles in Polyaxon - scheduling strategies"
meta_description: "A feature for injecting certain information into operations at compilation time to preset configuration for node scheduling, 
queue routing, resources requirements and definition, connections, and access level control."
tags:
    - namespace
    - queueing
    - pipelines
    - kubernetes
    - scheduling
sidebar: "core"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Run Profile is a feature for injecting certain information into operations at compilation time to preset configuration for node scheduling, 
queue routing, resources requirements and definition, connections, and access level control.

## Why using a run profile

It's possible to set for each operation an 
[environment section](/docs/core/specification/environment/), a [queue](/docs/core/specification/operation/#queue), a [container resources requirements](https://kubernetes.io/docs/concepts/containers/), 
a [termination](/docs/core/specification/termination/). But oftentimes, you might want to reuse some or all of these options 
and apply them to a certain type of operations. 

One way to achieve such workflow is to push as many configuration sections as possible to the components, but this is not always possible and it's not recommended, 
either because a component should be generic or the component should be used across different clusters, with different references for queues, nodes, ...

Polyaxon provides a concept called RunProfile, that you can use to package several information about how to preset your operations.

Users can just reference the profile in their [operations specification](/docs/core/specification/operation/#profile) or using the CLI/CLIENT `polyaxon run ... profile=my-profile`

## Managing run profiles

In order to create and manage run profiles, please check the [management section for more details](/docs/management/ui/run-profiles/)
