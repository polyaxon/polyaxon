---
title: "Features"
sub_link: "information/features"
meta_title: "Polyaxon Features - Core Concepts"
meta_description: "Polyaxon comes with powerful features built directly into the core software which are customizable and extensible to suit your needs."
visibility: public
status: published
tags:
  - concepts
  - quick-start
  - tutorials
  - features
sidebar: "intro"
---

![polyaxonfile architecture](../../../../content/images/references/specification/features.png)

Polyaxon comes with powerful features built directly into the core software which can be customized and configured based on the needs of each individual deployment.

Here's a quick overview of the core features you'll probably be interested in as you're getting started. This isn't an exhaustive list, just some highlights.


## Powerful workspace

Polyaxon provides a powerful and interactive workspace including:

- A command line interface
- SDKs and clients
- An extensive tracking API
- A dashboard with visualizations and advanced insights
- Lineage and provenance tracking
- Possibility to create custom dashboards and visualizations
- Advanced query & search interface
- Uniform logs management and streaming for all operations
- Jupyter Notebook & Jupyter Lab integration
- Matplotlib, Plotly, Bokeh, Altair, and Vega integrations
- Tensorboard integration
- VSCode integration
- Streamlit, Voila, Papermill, Commuter integrations
- Native Kubeflow scheduling
- Celery executor
- Built-in logic for building containers
- Customizable interface
- Unlimited scalability options
- Auto-management of artifacts and lineage tracking
- CI system for automating the training of your experiment based on different types of triggers.

## Reproducible results

Polyaxon makes your experiments reproducible, portable, and repeatable while being language and framework agnostic.

- Powerful packaging format `Polyaxonfile`: A specification for packaging dependencies, inputs, outputs, artifacts, environments, and runtime of an operation to schedule on Kubernetes.
- Extensive tracking API for source code, parameters, data, metrics, tags, and logs.
- You can see the full experiment history at a glance, including when, who, and where.
- Auto-document all experiments with statuses, metrics, hyperparams, source code, data, visualizations, artifacts, and resources used in each experiment.
- Advanced insights and comparison of experiments based on results, hyperparams, versions of training data and source code.


## Developer-friendly API

At its core, Polyaxon is a self-consuming, RESTful JSON API with decoupled clients and front-end.
We provide lots of tooling to improve data scientists work, but at the end of the day it's **Just JSON**️,
so if you want to use Polyaxon completely headless and write your own frontend or clients... you can!

Equally, Polyaxon is heavily designed for performance and scalability with replication and concurrency.


## Massive scale

You can easily scale Polyaxon API and scheduler horizontally, and with Polyaxon agents you can scale your workload over multiple namespaces and clusters.


## Built-in Flow engine

Polyaxon exposes a flow engine that enables users to author workflows and DAGs with well-thought-out features:
 * Queueing
 * Routing
 * Caching
 * Concurrency and parallelism
 * Native integration with team management, ACL, and RBAC rules
 * Native support for ML workload: Kubeflow Operators, Hyperparameter tuning, Ray jobs, Dask Jobs...


## Built-in Optimization engine

Polyaxon exposes an ensemble of hyperparameter tuning algorithms that can effectively optimize any model.

Our optimization engine is based on open-source tools, and can intelligently choose the best parameters for your problem by balancing exploration and exploitation of your parameter search space to obtain high-performing results.

With the robust scheduling provided by the platform, you can fully leverage and maximize your cluster resources and compute infrastructure,
to run a high number of parallel jobs and optimize experiments across up to thousands of workers.

## Components, Plugins, & integrations

Polyaxon components can be developed by anyone, we share some generic components in an open-source public hub,
and we welcome users to contribute more components.

And since Polyaxon's core is open-source, built as a JSON API, has webhooks, and gives you full control over your container workload:
It essentially integrates with absolutely everything.
Some things are easier than others, but almost anything is possible with a little scripting.

You can browse our [directory of integrations](/integrations/) with instructions, or build any custom integration yourself.

Polyaxon provides an event based abstraction to alter the internal work, and so you can build your own scheduler for example.

## Roles & permissions

Deploy Polyaxon with sensible user roles and permissions from the start.

- **Outsiders:** Outsider is a person who isn't explicitly a member of your organization, but who has Read, Write, or Admin permissions to one or more projects in your organization.
- **Viewers:** Viewers can view experiments/jobs/services, as well as view most other data within the organization.
- **Members:** Members can view and act on experiments/jobs/services, as well as view most other data within the organization.
- **Admins:** Admin privileges on any teams of which they\'re a member. They can create new teams and projects, as well as remove teams and projects which they are already admin of.
- **Managers:** Gains admin access on all teams as well as the ability to add and remove members.
- **Billing:** Can see/edit billing information and subscription details only.
- **Owners:** Gains full permission across the organization. Can manage members as well as perform catastrophic operations such as removing the organization.

Polyaxon also comes with a concept called `Team` that allows you to promote a user role on specific teams,
e.g. an organization wide viewer can have the member or admin role on a specific team.
All projects that authorize that team will give the additional permissions to that user with the global viewer role.

## Queuing & Scheduling

Polyaxon supports several scheduling strategies based on node management and queues routing.
Queues in Polyaxon provides an abstraction to manage how your resources can be accessed, every queue has a priority and a concurrency limit.
