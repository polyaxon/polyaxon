---
title: "Architecture"
sub_link: "information/architecture"
meta_title: "Polyaxon Architecture - Core Concepts"
meta_description: "Polyaxon is structured as a modern, decoupled, micro-services oriented platform. Discover how things fit together at Polyaxon."
visibility: public
status: published
tags:
  - concepts
  - quick-start
  - architecture
sidebar: "intro"
---

## Core Architecture

Polyaxon is structured as a modern, decoupled, micro-service oriented architecture.


1. **A robust core JSON API**
2. **An Asynchronous, customizable, and scalable scheduler**
3. **An extensive tracking API**
4. **An event/action oriented interface**
5. **A pipeline engine capable of authoring workflows as directed acyclic graphs (DAGs)**
6. **An optimization engine to search automatically and concurrently for the best hyperparameters in a search space based on state of the art algorithms**
7. **A CI system to trigger experiments/hyperparameter tuning/pipelines automatically based on some event and track their execution and report results to users**

These components work together to make every Polyaxon deployment function smoothly,
but because they're decoupled there's plenty of room for customization.

In fact, users can decide for example to deploy only the core and using an external tracking service, or replace the built-in scheduler, pipeline, and optimization engine with other platforms.


## How things fit together

![Polyaxon Architecture](../../../../content/images/concepts/architecture/polyaxon_architecture.png)

Polyaxon relies on several components to function smoothly:

 * Postgres database
 * redis
 * rabbitmq
 * connections: docker registries, artifacts stores, git connections, ...

Polyaxon schedules your workload to Kubernetes, so you will need:

 * Kubernetes cluster(s) for deploying one or several Polyaxon Agents


## Polyaxon platform

In order to understand how Polyaxon can help you organize your workflow,
you need to understand how Polyaxon abstract the best practices of data science job.

![Polyaxon platform](../../../../content/images/concepts/architecture/polyaxon_platform.png)

Polyaxon runs both in the cloud and on-premise, and provides access via:

 * Polyaxon command line interface
 * Polyaxon dashboard
 * Polyaxon SDKs targeting the Polyaxon API
 * Polyaxon Webhooks


These interfaces hide the powerful abstractions provided by the Polyaxon architecture.
When a machine learning engineer or a data scientist schedules a job or an experiment,
Polyaxon relies on Kubernetes for:

 * Managing the resources of your cluster (Memory, CPU, GPU, TPU, ...)
 * Creating easy, repeatable, portable deployments
 * Scaling up and down as needed

Polyaxon does the heavy lifting of:

 * Exposing a rich runtime including jobs, services, distributed jobs
 * Scheduling operations
 * Automation with a flow engine and an optimization engine
 * Resolving dependencies between operations
 * Validating and authorizing access to resources, connections, namespaces
 * Creating docker images
 * Monitoring the statuses and resources
 * Streaming logs
 * Tracking code version, params, logs, configurations, and tags
 * Reporting metrics and outputs and other results to the user
 * Driving insights, knowledge, and analytics about your experiments
 * Exposing a rich workspace based on Notebooks, Streamlit, VSCode, ...
