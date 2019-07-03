---
title: "Polyaxon Pipeline Engine: Polyflow"
sub_link: "polyflow"
meta_title: "Polyaxon Pipeline Engine: Polyflow - Polyaxon References"
meta_description: "Running pipelines is often important to optimize an build strong models."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
    - hyperparams-optimization
sidebar: "polyflow"
---

> Polyflow is in beta, please reach out to us if you want to have early access

## Overview 

Polyflow is an open source project that provides container-native engine for running pipelines on Kubernetes. 
Each operation in a Polyflow pipeline is defined as pod running a main container defined by the user.

Often times, Polyaxon's users tend to run complex jobs and experiment that depend on each other. 
Polyaxon define a several primitive that can run independently, each one of these primitives is a mini-pipeline. For example example: 
 * An experiment requires a build to prepare a docker image before running
 * An hyperparameters group run several experiments and follow their progress
 
Polyflow is an extension to these primitive to allow the users to automate workflows and define complex interactions. 

## Features

 * Easy-to-use: Polyflow is easy to use and does not extra complexity or extra dependencies to a cluster already running Polyaxon.
 * Scalability: Polyflow scales similarly to Polyaxon, defines extra API endpoints, and reuses same logic for scheduling and monitoring runs.
 * Flexibility: Similar to Polyaxon, Polyflow allows users to run anything that can be run in a container.
 * Reusability: Polyflow introduces some notions that will allow several teams to operationalize and reuse several logic and package them as templates/actions/events. 
 * Kubernetes and Polyaxon Native: Polyflow integrates natively with Polyaxon and reuses it's components, and it also allows to leverage Kubernetes services such as volumes, secrets, and RBAC.
 * Interoperability: Polyflow similar to Polyaxon, has a native backend, but can be used to leverage other backends: e.g. airflow.

## Concepts

 * [Templates](/references/polyflow/templates/)
 * [Actions/Events](/references/polyflow/actions-events/)
 * [Pipelines](/references/polyflow/pipelines/)
 * [Schedules](/references/polyflow/pipelines/#schedules)

## Example

Here's a simple example running a pipeline using Polyflow:

```yaml
version: 1

kind: pipeline

name: test-pipeline

schedule:
  kind: interval
  start_at: '2019-06-24T21:20:07+00:00'
  frequency: 120
  depends_on_past: true

ops:
  - name: job1
    template: {name: job-template}
    params:
      bucket: s3://bucket-with-data
  - name: deep-wide-experiment
    template: {action: deep-wide-model}
    dependencies: [job1]
    params:
      lr: 0.05

templates:
  - kind: job
    name: job-template
    inputs:
    - name: input-bucket
      type: s3_path
    build: {'dockerfile': 'dockerfiles/Dockerfile'}
    environment:
      node_selector: {polyaxon: experiments}
      service_account: my-service
      secret_refs: [s3-secret]
      max_restarts: 2
```

This is a recurrent pipeline that executes 2 operation one after another, one operation is a job defined inline as a template, and the other one is an experiment defined in the actions registry.

