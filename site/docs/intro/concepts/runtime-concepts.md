---
title: "Runtime Concepts"
sub_link: "concepts/runtime-concepts"
meta_title: "Polyaxon Runtime/Jobs/Services/Notebooks/Tensorboard/DAGs/Hyperparameter Tuning - Core Concepts"
meta_description: "Polyaxon schedules and manage the lifecycle of several runtimes."
visibility: public
status: published
tags:
  - architecture
  - concepts
  - polyaxon
sidebar: "intro"
---

Polyaxon relies on a set of concepts to manage the experimentation and the automation process.
In this section, we provide a high-level introduction to these concepts,
with more details in pages dedicated to each concept.

### Runtime of a Component

A `component` is the model that describes the discrete and containerized logic you want to run,
they optionally take inputs, perform some work, and optionally return some outputs.

Components can process data directly, train a model, or orchestrate external systems, they can be built using any programming language.
There are almost no restrictions on what a component can do.

Furthermore, each component receives metadata about its environment and upstream dependencies (if it's defined in a DAG) before it runs,
it's called the [context](/docs/core/context/), even if it does not receive any explicit data inputs,
giving it an opportunity to change its behavior depending on the context it's running inside.

Since Polyaxon runs containers, it is agnostic to the code each component runs and there are no restrictions on what inputs and outputs can be.

<blockquote class="light">Please refer to <a href="/docs/core/specification/component/">core/specification/component</a>
to learn about the component specification and <a href="/docs/management/component-hub/">management/Component Hub</a> for details about the Component Hub.</blockquote>

Each component can have one runtime that it's specified in the [run section of a component](/docs/core/specification/component/#run).
Polyaxon supports several runtimes:
 * Jobs
 * Distributed Jobs
 * Services
 * DAGs

### Job

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
 * [RayJob](/docs/experimentation/distributed/ray-jobs/)
 * [DaskJob](/docs/experimentation/distributed/dask-jobs/)

<blockquote class="light">Please refer to <a href="/docs/experimentation/distributed/">experimentation/distrbuted-jobs</a> for more details.</blockquote>

### Service

A `service` allows to run dashboards, apps, and APIs.

A service can be:

 * A Tensorboard.
 * A Notebook.
 * A custom dashboard.
 * A Streamlit app.
 * A container exposing an API.

<blockquote class="light">Please refer to <a href="/docs/experimentation/services">experimentation/services</a> for more details.</blockquote>

### DAG

A `DAG` is a powerful tool to describe dependencies between operations,
it allows to author a directed acyclic graph of operations with first class support for states and artifacts dependencies.

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

A `matrix` is an automatic and practical way to run a component with different parameters based on a mapping or a hyperparameter search algorithm.


<blockquote class="light">
Please refer to <a href="/docs/automation/optimization-engine/">automation/optimization-engine</a> and <a href="/docs/automation/mapping/">automation/mapping</a> for more details.
</blockquote>
