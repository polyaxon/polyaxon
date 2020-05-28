---
title: "Concepts"
sub_link: "introduction/concepts"
meta_title: "Polyaxon Architecture - Core Concepts"
meta_description: "Polyaxon is structured as a modern, decoupled, micro-services oriented platform. Discover how things fit together at Polyaxon."
visibility: public
status: published
tags:
    - architecture
    - concepts
    - polyaxon
sidebar: "core"
---

Polyaxon relies on a set of concepts to manage the experimentation and the automation process,
in this section we provide a high level introduction to these concepts,
with more details in pages dedicated to each concept.


### User

A `User` is the entity that creates projects, starts experiments, creates jobs and pipelines, manages teams and clusters.

<blockquote class="light">Please refer to <a href="/docs/management/ui/users/">management/users</a> for more details.</blockquote>

### Organization

An `Organization` is the entity that enables several users to collaborate across many projects at once.
Owners and admins can manage member access to the organization's data and projects with sophisticated security and administrative features.

<blockquote class="light">Please refer to <a href="/docs/management/ui/organizations/">management/organizations</a> for more details.</blockquote>

### Team

A `Team` provides a way to manage groups of users, their access roles, and resources quotas and permissions.

<blockquote class="light">Please refer to <a href="/docs/management/ui/teams/">management/teams</a> for more details.</blockquote>

### Project

A `Project` in Polyaxon is very similar to a project in GitHub,
it aims at organizing your efforts to solve a specific problem.
A project consist of a name and a description, access to several connections and data, and components to execute.

<blockquote class="light">Please refer to <a href="/docs/management/ui/projects/">management/projects</a> for more details.</blockquote>

### Component

A `component` is the model that describes the discrete and containerized logic you want to run, 
they optionally take inputs, perform some work, and optionally return some outputs.

Components can process data directly, train a model, or orchestrate external systems, they can be built using any programming language. 
There are almost no restrictions on what a component can do.

Furthermore, each component receives metadata about its environment and upstream dependencies (if it's defined in a DAG) before it runs, 
it's called the [context](/docs/core/specification/context/), even if it does not receive any explicit data inputs, 
giving it an opportunity to change its behavior depending on the context it's running inside.

Since Polyaxon runs containers, it is agnostic to the code each component runs and there are no restrictions on what inputs and outputs can be.

<blockquote class="light">Please refer to <a href="/docs/core/specification/component/">core/specification/component</a> 
to learn about the component specification and <a href="/docs/management/component-hub/">management/Component Hub</a> for details about the Component Hub.</blockquote>

Each component can have one runtime that it's specified in the [run section of a component](/docs/core/specification/component/#run).
Polyaxon supports several runtimes:


#### Job

A `job` is the execution of your code with data/connections and the provided parameters on the Kubernetes cluster.

A Job can be:
 
 * A machine learning experiment.
 * A data processing job.
 * An ETL task.
 * A container build job.

<blockquote class="light">Please refer to <a href="/docs/experimentation/jobs/">experimentation/jobs</a> for more details.
</blockquote>

### Distributed Jobs

Polyaxon supports distributed jobs for model training or data processing via several Kubernetes operators:

 * [TFJob](/docs/experimentation/distributed/tf-jobs/)
 * [MpiJob](/docs/experimentation/distributed/mpi-jobs/)
 * [PytorchJob](/docs/experimentation/distributed/pytorch-jobs/)
 * [SparkJob](/docs/experimentation/distributed/spark-jobs/)
 * [DaskJob](/docs/experimentation/distributed/dask-jobs/)

<blockquote class="light">Please refer to <a href="/docs/experimentation/distributed/">experimentation/distrbuted-jobs</a> for more details.</blockquote>

#### Service

A `service` allows to run dashboards, apps, and apis.

A service can be:
 
 * A tensorboard.
 * A notebook.
 * A custom dashboard.
 * A streamlit app.
 * A container exposing an API.

<blockquote class="light">Please refer to <a href="/docs/experimentation/services">experimentation/services</a> for more details.</blockquote>

#### DAG

A `DAG` is a powerful tool to describe dependencies between operations, 
it allows to author a directed acyclic graph of operation with first class support for states and artifacts dependencies.

<blockquote class="light">Please refer to <a href="/docs/automation/flow-engine/">automation/flow-engine</a> for more details.</blockquote>


### Operation

An `operation` is how you execute your components, it allows you to:
 
 * pass the parameters for required inputs or override the default values of optional inputs.
 * patch the definition of the component to set environments, initializers, and resources.
 * set termination logic and retries.
 * set trigger logic to start a component in a pipeline context.
 * parallelize or map the component over a matrix of parameters.
 * put an operation on a schedule.
 * subscribe a component to events to trigger executions automatically.

<blockquote class="light">
Please refer to <a href="/docs/core/specification/operation/">core/specification/operation</a> and <a href="/docs/management/runs-dashboard/">management/Runs Dashboard</a> to learn about the operation specification.
</blockquote>

 
### Matrix

A `matrix` is an automatic and practical way to run an component with different hyper parameters based on a mapping or a hyperparameters search algorithm.


<blockquote class="light">
Please refer to <a href="/docs/automation/optimization-engine/">automation/optimization-engine</a> and <a href="/docs/automation/mapping/">automation/mapping</> for more details.
</blockquote>


### Schedules

Although you can run your operation at any time, for any reason, it is often useful to automate and run your components at certain times using a `schedule`. 

<blockquote class="light">Please refer to <a href="/docs/automation/optimization-engine/">automation/schedules</a> for more details.</blockquote>


### Run Profile

A `run Profile` allows admin to preset several meta information about runs, e.g. node scheduling and routing, which facilitate attaching quotas to a user/team/project, 
so that the entities they create, i.e. builds/jobs/experiments/notebooks, cannot exceed the parallelism and may not consume more 
resources than the quota specification allows.

<blockquote class="light">Please refer to <a href="/docs/core/scheduling-strategies/run-profiles/">scheduling-strategies/run-profiles</a> and <a href="/docs/management/ui/run-profiles/">management/run-profiles</a> for more details.</blockquote>
