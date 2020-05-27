---
title: "Features"
sub_link: "introduction/features"
meta_title: "Polyaxon Features - Core Concepts"
meta_description: "Polyaxon comes with powerful features built directly into the core software which are customisable and extensible to suit your needs."
visibility: public
status: published
tags:
    - concepts
    - quick-start
    - tutorials
    - features
sidebar: "core"
---

Polyaxon comes with powerful features built directly into the core software which can be customised and configured based on the needs of each individual deployment.

Here's a quick overview of the core features you'll probably be interested in as you're getting started. This isn't an exhaustive list, just some highlights.


## Powerful workspace

Polyaxon provides a powerful and interactive workspace including:

- A command line interface
- SDKs and clients
- An extensive tracking api
- A dashboard with visualisations and advanced insights
- Possibility to create custom dashboards and visualisations
- Advanced Query & search interface
- Notebooks integration
- Tensorboards integration
- CI system for automating the training of your experiment based on different types of triggers.

## Reproducible results

Polyaxon makes your experiments reproducible, portable, and repeatable while being language and framework agnostic. 
It has a tracking api for source code, parameters, data, metrics, tags, and logs.


- You can see the full experiment history at a glance, including when, who and where.
- Auto-document all experiments with statuses, metrics, hyperparams, source code, data, visualizations, artifacts and resources used in each experiment.
- Advanced insights and comparison of experiments based on results, hyperparams, versions of training data and source code.


## Developer-friendly API

At its core Polyaxon is a self-consuming, RESTful JSON API with decoupled clients and front-end. 
We provide lots of tooling to improve data scientists work, but at the end of the day it's **Just JSON**️, 
so if you want to use Polyaxon completely headless and write your own frontend or clients... you can!

Equally, Polyaxon is heavily designed for performance and scalability with replication and concurrency.


## Massive scale

You can easily scale Polyaxon API and scheduler horizontally, and with Polyaxon agents you can scale your workload over multiple namespaces and clusters.


## Built-in Flow engine

Polyaxon exposes a flow engine that enables users to author workflows and DAGs. 


## Built-in Optimization engine

Polyaxon exposes an ensemble of hyperparameters tuning algorithms that can effectively optimize any model.

Our optimization engine is based on open-source tools, and can intelligently chooses the best parameters for your problem by balancing exploration and exploitation of your parameter search space to obtain high-performing results.

With the robust scheduling provided by the platform, you can fully leverage and maximize your cluster resources and compute infrastructure, 
to run a high number of parallel jobs and optimize experiments across up to thousands of workers. 

## Components, Plugins, & integrations

Polyaxon components can be developed by anyone, we share some generic components in an open source public hub, 
and we welcome users to contribute more components. 

And since Polyaxon's core is open-source, built as a JSON API, has webhooks, and gives you full control over your container workload: 
It essentially integrates with absolutely everything. 
Some things are easier than others, but almost anything is possible with a little scripting.

You can browse our [directory of integrations](/integrations/) with instructions, or build any custom integration yourself.

Polyaxon provides an event based abstraction to alter the internal work, and so you can build you own scheduler for example.

## Roles & permissions

Deploy Polyaxon with sensible user roles and permissions from the start.

- **Outsiders:** Outsider is a person who isn't explicitly a member of your organization, but who has Read, Write, or Admin permissions to one or more project in your organization.
- **Members:** Members can view and act on experiments/jobs/services, as well as view most other data within the organization.
- **Admins:** Admin privileges on any teams of which they\'re a member. They can create new teams and projects, as well as remove teams and projects which they are already admin of.
- **Managers:** Gains admin access on all teams as well as the ability to add and remove members.
- **Owners:** Gains full permission across the organization. Can manage members as well as perform catastrophic operations such as removing the organization.


## Queuing & Scheduling

Polyaxon supports several scheduling strategies based on node management and queues routing. 
Queues in Polyaxon provides an abstraction to manage how your resources can be accessed, every queue has a priority and a concurrency limit.

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
but because they're decoupled there's plenty of room for customisation.

In fact users can decide for example to deploy only the core and using an external tracking service, or replace the built-in scheduler, pipeline, and optimization engine with other platforms.

---

## How things fit together

![Polyaxon Architecture](../../../../content/images/concepts/architecture/polyaxon_architecture.png)

Polyaxon relies on several components to function smoothly:

 * Postgres database
 * redis
 * rabbitmq
 * connections: docker registries, artifacts stores, git connections, ... 

Polyaxon schedules your workload to Kubernetes, so you will need:

 * Kubernetes cluster(s) for deploying one or several Polyaxon Agents
 
---

## Polyaxon platform

In order to understand how Polyaxon can help you organize your workflow,
you need to understand how Polyaxon abstract the best practices of data science job.

Polyaxon runs both in the cloud and on premise, and provides access via:

 * Polyaxon command line interface
 * Polyaxon dashboard
 * Polyaxon SDKs targeting the Polyaxon api
 * Polyaxon Webhooks


These interfaces hide the powerful abstractions provided by the Polyaxon architecture.
When a machine learning engineer or a data scientist schedules a job or an experiment,
Polyaxon relies on Kubernetes for:

 * Managing the resources of your cluster (Memory, CPU, GPU, TPU, ...)
 * Creating easy, repeatable, portable deployments
 * Scaling up and down as needed

Polyaxon does the heavy lifting of:

 * Scheduling the jobs
 * Resolving dependencies between operations
 * Validating and authorizing access to resources, connections, namespaces
 * Creating docker images
 * Monitoring the statuses and resources
 * Tracking code version, params, logs, configurations, and tags
 * Reporting metrics and outputs and other results to the user

![Polyaxon platform](../../../../content/images/concepts/architecture/polyaxon_platform.png)
