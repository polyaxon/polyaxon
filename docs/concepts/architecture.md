---
title: "Architecture"
sub_link: "architecture"
meta_title: "Polyaxon Architecture - Core Concepts"
meta_description: "Polyaxon is structured as a modern, decoupled, micro-services oriented platform. Discover how things fit together at Polyaxon."
visibility: public
status: published
tags:
    - architecture
    - concepts
    - polyaxon
sidebar: "concepts"
---

Polyaxon is structured as a modern, decoupled, micro-service oriented architecture.


1. **A robust core JSON API**
2. **An Asynchronous, customizable, and scalable scheduler**
3. **An extensive tracking API**
4. **An event/action oriented interface**
5. **A pipeline engine capable of authoring workflows as directed acyclic graphs (DAGs)**
6. **An optimization engine to search automatically and concurrently for the best hyperparameters in a search spaces based on state of the art algorithms**
7. **A CI system to trigger experiments/hyperparams tuning/pipelines automatically based on some event and track there execution and report results to users**

These components work together to make every Polyaxon deployment function smoothly, 
but because they're decoupled there's plenty of room for customisation.

In fact users can decide for example to deploy only the core and tracking API, and replace the built-in scheduler, pipeline, and optimization engine with other platforms.

---

## How things fit together

![Polyaxon Architecture](../../content/images/concepts/architecture/polyaxon_architecture.png)

Polyaxon relies on several components to function smoothly:

 * Postgres database
 * redis
 * rabbitmq
 * docker registries
 * Storage for [data](/configuration/custom-data-storage/)/[outputs](/configuration/custom-outputs-storage/)/[logs](/configuration/custom-logs-storage/)

Depending on the version you are deployment, you may need as well:

 * Kubernetes cluster(s) for deploying Polyaxon
 * Docker, Docker compose, or a container management platform for deploying a scalable Polyaxon (tracking only) version
 * Linux station for installing the platform from source
 
---

## Polyaxon platform

In order to understand how Polyaxon can help you organize your workflow,
you need to understand how Polyaxon abstract the best practices of data science job.

Polyaxon runs both in the cloud and on premise, and provides access via:

 * Polyaxon command line interface
 * Polyaxon dashboard
 * Polyaxon SDKs targeting the Polyaxon api
 * Polyaxon Webhooks


These interfaces hides the powerful abstraction provided by the Polyaxon architecture.
When a machine learning engineer or a data scientist deploys a model,
Polyaxon relies on Kubernetes for:

 * Managing the resources of your cluster (Memory, CPU, and GPU)
 * Creating an easy, repeatable, portable deployments
 * Scaling up and down as needed

Polyaxon does the heavy lifting of:

 * Scheduling the jobs
 * Versioning the code
 * Creating docker images
 * Monitoring the statuses and resources
 * Tracking params, logs, configurations, and tags
 * Reporting metrics and outputs and other results to the user

The choice of using Docker containers to run jobs is important,
it provides the user a wide range of possibilities to [customize the run environment](/configuration/custom-run-environment/)
to fit the requirements and dependencies needed for the experiments.

![Polyaxon platform](../../content/images/concepts/architecture/polyaxon_platform.png)

---

## Polyaxon Concepts

Polyaxon relies on a set of concepts to manage the experimentation process,
in this section we provide a high level introduction to these concepts,
with more details in pages dedicated to each concept.


### User

A `User` is the entity that creates projects, starts experiments, creates jobs and pipelines, manages teams and clusters.
A `User` has a set of permissions, and can be normal user or superuser.

> Please refer to the [users management section](/configuration/users-management/) for more details.

### Teams & Organizations

A `Team` provides a way to manage group of users, their access roles, and resources quotas.

<blockquote class="warning"> This entity exists only on Polyaxon EE version</blockquote>

### Resources quotas

When a `quota` is attached to a user/team/project, the entity created, i.e. builds/jobs/experiments/notebooks, cannot exceed the parallelism and may not consume more 
resources than the quota specification allows.

<blockquote class="warning"> This entity exists only on Polyaxon EE version</blockquote>

### Project

A `Project` in Polyaxon is very similar to a project in github,
it aims at organizing your efforts to solve a specific problem.
A project consist of a name and a description, the code to execute, the data, and a polyaxonfile.yml.

> Please refer to the [projects section](/concepts/projects/) for more details.

### Experiment

An `Experiment` is the execution of your model with data and the provided parameters on the cluster.

A `Experiment Job` is the Kubernetes pod running on the cluster for a specific experiment,
if an experiment runs in a distributed way it will create multiple instances of `Experiment Job`.

> Please refer to the [experiments section](/concepts/experiments/) for more details.


### Experiment Group

An `Experiment Group` provide 2 interfaces:
  * An automatic and practical way to run a version of your model and data with different hyper parameters based on a hyperparameters search algorithm.
  * A selection of experiments to compare.

> Please refer to the [experiment groups - selection](/concepts/experiment-groups-selections/) for more details on how to create group selections
 
> Please refer to the [experiment groups - hyperparameters optimization](/concepts/experiment-groups-hyperparameters-optimization/) for more details on how to run hyperparametres search.


### Job

A `Job` is the execution of your code to do some data processing or any generic operation.

> Please refer to the [jobs section](/concepts/jobs/) for more details.

### Build Job

A `BuildJob` is the process of creating containers, Polyaxon provides different backends for creating containers.

> Please refer to the [build jobs section](/concepts/builds/) for more details.


### Tensorboard

A `Tensorboard` is a job running to visualize the metrics of an experiment,
the metrics of all experiments created during a hyperparameters-optimization group, 
the metrics of all experiment in a selection group, or the experiments of a project.

> Please refer to the [tensorboards](/concepts/tensorboards/) for more details.

### Notebooks

A `Notebooks` is a job running project wide to provide an fast and easy way to explore data, start experiments. 
Polyaxon provides different backend to start notebooks, or Jupyter Labs.

> Please refer to the [project notebooks§§](/concepts/notebooks/) for more details.


### Checkpointing, resuming and restarting experiments

Checkpointing is a very important concept in machine learning, it prevents losing progress.
It also provide the possibility to resume an experiment from a specific state.

Polyaxon provides some structure and organization regarding checkpointing and outputs saving.


> Please refer to the [save, resume & restart](/concepts/save-resume-restart/) for more details.
