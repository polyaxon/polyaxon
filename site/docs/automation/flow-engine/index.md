---
title: "Flow Engine"
sub_link: "flow-engine"
meta_title: "Polyaxon Pipeline is a Flow Engine - Polyaxon References"
meta_description: "Running pipelines is often important to optimize and build strong models."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - automation
  - workflow
  - pipelines
sidebar: "automation"
---

## Overview

Polyaxon DAGs is a tool that provides a container-native engine for running machine learning pipelines on Polyaxon.
A DAG manages multiple operations with dependencies.
Each operation in a DAG (directed acyclic graph) is defined by its component runtime.
This means that operations in a DAG can be jobs, services, distributed jobs, parallel executions, or nested DAGs.

Oftentimes, Polyaxon's users tend to run complex jobs and experiments that depend on each other.
Polyaxon defines main primitives, Component/Operation, that can run independently.
The flow engine is an extension to these primitives to allow the users to automate workflows and define complex interactions.

Polyaxon DAGs can be used with other Polyaxon experimentation and automation features:

 * They can run and orchestrate [jobs](/docs/experimentation/jobs/), [distributed jobs](/docs/experimentation/distributed/), and [services](/docs/experimentation/services/).
 * They can leverage all [pipeline helpers](/docs/automation/helpers/).
 * They can run in parallel and can be used with [mapping](/docs/automation/mapping/) or other [optimization algorithms](/docs/automation/optimization-engine/).
 * They can run on [schedule](/docs/automation/schedules/)
 * They can subscribe to [events](/docs/automation/events/)

## Features

Polyaxon flow engine provides several features to reduce the complexity and increase the productivity of Polyaxon users:

 * Easy-to-use: It is easy to use and does not add any extra complexity or extra dependencies to a cluster already running Polyaxon.
 * Scalability: It scales massively with scheduling and routing capabilities, it defines extra API endpoints, and it reuses the same logic for tracking and monitoring runs.
 * Flexibility: It allows users to run anything that can be run in a container.
 * Reusability: A Dag is a runtime of a component, they can be parameterized and shared like any other component, all operations in a DAG are also running other components which means you can reuse common logic.
 * Kubernetes and container Native: It integrates natively with the rest of Polyaxon and reuses its components, which allows you to leverage Kubernetes services such as volumes, secrets, and RBAC, as well as concepts such as routes and connections.
 * Interoperability: It can be used to leverage and interact with external systems.

## Specification

Please check the [DAG specification](/docs/automation/flow-engine/specification/) guide to learn about all details for DAGs in Polyaxon.

## Example

Here's a simple example of running a pipeline using Polyflow:

```yaml
version: 1
kind: component
name: test-pipeline

ops:
  - name: job1
    dagRef: job-template
    params:
      bucket: s3://bucket-with-data
  - name: deep-wide-experiment
    hubRef: deep-wide-model
    dependencies: [job1]
    params:
      lr: 0.05

components:
  - name: job-template
    inputs:
    - name: input-bucket
      type: s3
    environment:
      nodeSelector: {polyaxon: experiments}
      serviceAccount: my-service
    run:
      kind: job
      container:
        name: data-processing-image
        command: [run.sh]
        args: ["--input-bucket"]
```

This is a pipeline that executes two operations one after another, one operation is a job defined inline, and the other one is a component defined in the Component Hub.

