---
title: "Features"
sub_link: "features"
meta_title: "Polyaxon Features - Core Concepts"
meta_description: "Polyaxon comes with powerful features built directly into the core software which are customisable and extensible to suit your needs."
visibility: public
status: published
tags:
    - concepts
    - quick-start
    - tutorials
    - features
sidebar: "concepts"
---

Polyaxon comes with powerful features built directly into the core software which can be customised and configured based on the needs of each individual deployment.

Here's a quick overview of the core features you'll probably be interested in as you're getting started. This isn't an exhaustive list, just some highlights.


## Powerful workspace

Polyaxon provides a powerful and interactive workspace including:

- A command line interface
- SDKs and clients
- An extensive tracking api for in-cluster and on other platforms workloads
- A dashboard with visualisations and advanced insights 
- Advanced Query & search interface
- Notebooks integration
- Tensorboards integration
- CI system for automating training of your experiment based on different types of triggers.

## Reproducible results

Polyaxon makes your experiments reproducible and repeatable while being language and framework agnostic. 
It has a tracking api for source code, parameters, data, metrics, tags, and logs.


- You can see the full experiment history at a glance, including when, who and where.
- Auto-document all experiments with statuses, metrics, hyperparams, source code, data, visualizations, artifacts and resources used in each experiment.
- Advanced insights and comparison of experiments based on results, hyperparams, versions of training data and source code.


## Developer-friendly API

At its core Polyaxon is a self-consuming, RESTful JSON API with decoupled clients and front-end. 
We provide lots of tooling to improve data scientists work, but at the end of the day it's **Just JSON**️, 
so if you want to use Polyaxon completely headless and write your own frontend or clients... you can!

Equally, Polyaxon is heavily designed for performance and scalability with replication and concurrency.


## Built-in Optimization engine

Polyaxon exposes an ensemble of hyperparameters tuning algorithms that can effectively optimize any model.

Our optimization engine intelligently chooses the best parameters for your problem by balancing exploration and exploitation of your parameter search space to obtain high-performing results.

With the robust scheduling provided by the platform, you can fully leverage and maximize your cluster resources and compute infrastructure, 
to run a high number of parallel jobs and optimize experiments across up to thousands of workers. 


## Plugins & integrations

Because Polyaxon is completely open source, built as a JSON API, has webhooks, and gives you full control over the front-end: It essentially integrates with absolutely everything. 
Some things are easier than others, but almost anything is possible with a little scripting.

You can browse our [directory of integrations](/integrations/) with instructions, or build any custom integration yourself.

Polyaxon provides an event based abstraction to alter the internal work, and so you can build you own scheduler for example.

## Roles & permissions

Deploy Polyaxon with sensible user roles and permissions from the start.


### Polyaxon CE

- **Admins:** Admins have access to all projects and are responsible for managing who can use the platform, therefor they are responsible to accept or reject new users.
- **Users:** Users are allowed to access in read/write mode their own projects and experiments, additionally they can access in read mode public projects from other users.
 
### Polyaxon EE 

- **Members:** Members can view and act on experiments/jobs/builds, as well as view most other data within the organization.
- **Admins:** Admin privileges on any teams of which they\'re a member. They can create new teams and projects, as well as remove teams and projects which they are already admin of.
- **Managers:** Gains admin access on all teams as well as the ability to add and remove members.
- **Owners:** Gains full permission across the organization. Can manage members as well as perform catastrophic operations such as removing the organization.


## Quotas (EE only)

Manage who can access what resources in your cluster, set parallelism quotas per users and projects.

## Dynamic configuration (EE only)

 * Update your Polyaxon deployment from UI interface, i.e. no need redeploy/upgrade to change the platform's configuration.
 * Override default cluster configuration per projects and teams

---

If you're curious to see more, check out the [features page](https://polyaxon.com/features/) on polyaxon.com.
