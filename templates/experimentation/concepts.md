# Polyaxon Architecture

In order to understand how to organize your workflow,
we need to understand how Polyaxon abstract the best practices of a data scientist job.

Polyaxon runs both in the cloud and on premise, and provides access via:

 * Polyaxon command line interface
 * Polyaxon dashboard
 * Polyaxon sdk targeting the Polyaxon api


These interfaces hides the powerful abstraction provided by the Polyaxon architecture.
When a machine learning engineer or data scientist deploy a model,
Polyaxon relies on Kubernetes for:

 * Managing the resources of your cluster (Memory, CPU, and GPU)
 * Creating an easy, repeatable, portable deployments
 * Scaling up and down as needed

Polyaxon does the heavy lifting of:

 * Scheduling the jobs
 * Versioning the code
 * Creating docker images
 * Monitoring the statuses and resources
 * Reporting back the results to the user

The choice of using Docker containers to run your jobs is important,
it provides the user a wide range of possibilities to [customize the run run environment](customization/customize_run_environment)
to fit the requirements and dependencies needed for the experiments.

![Screenshot](/images/polyaxon_architecture.png)


# Concepts

Polyaxon relies on a set of concepts to manage an experimentation workflow,
in this section we provide a high level introduction to these concepts,
with more details in page dedicated to each concept.


## User

A `User` is the entity that creates project, starts experiments, manages organizations and clusters.
A `User` has a set of permissions, and can be an normal user or superuser.

!!! note
    Please refer to the [management section](management/introduction) for more details.

## Organization

An `Organization` provides a way to manage team/group of users, their access roles, and resources quotas.

!!! caution
    This is still a work in progress.

## Project

A `Project` in Polyaxon is very similar to a project in github,
it aims at organizing your efforts to solve a specific problem.
A project consist of a name and a description, the code to execute, the data, and a polyaxon.yaml.

!!! note
    Please refer to the [projects section](experimentation/project) for more details.

## Experiment Group

An `Experiment Group` is a way to try a version of code and data with different hyper parameters.

!!! note
    Please refer to the [experiment groups and hyper parameters search section](experimentation/experiment_group) for more details.

## Experiment

An `Experiment` is the execution of your model with data and the provided parameters on the cluster.

!!! note
    Please refer to the [experiments and distributed runs section](experimentation/experiment) for more details.

## Job

A `Job` is the pod running on the cluster for a specific experiment,
if an experiment run in a distributed way it will create multiple instances of `Job`.

!!! note
    Please refer to the [jobs section](experimentation/job) for more details.
