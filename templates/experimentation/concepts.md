## Polyaxon Architecture

In order to understand how Polyaxon can help you organize your workflow,
you need to understand how Polyaxon abstract the best practices of data science job.

Polyaxon runs both in the cloud and on premise, and provides access via:

 * Polyaxon command line interface
 * Polyaxon dashboard
 * Polyaxon sdk targeting the Polyaxon api


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
 * Reporting back the results to the user

The choice of using Docker containers to run your jobs is important,
it provides the user a wide range of possibilities to [customize the run run environment](/customization/customize_run_environment)
to fit the requirements and dependencies needed for the experiments.

![architecture](/images/polyaxon_architecture.png)


## Concepts

Polyaxon relies on a set of concepts to manage an experimentation workflow,
in this section we provide a high level introduction to these concepts,
with more details in pages dedicated to each concept.


### User

A `User` is the entity that creates project, starts experiments, manages teams and clusters.
A `User` has a set of permissions, and can be normal user or superuser.

!!! info "More details"
    Please refer to the [management section](/management/introduction) for more details.

### Teams

An `Team` provides a way to manage team/group of users, their access roles, and resources quotas.

!!! caution
    This is still a work in progress.
    If you want to be notified when we release this feature, please subscribe to receive our progress.

### Project

A `Project` in Polyaxon is very similar to a project in github,
it aims at organizing your efforts to solve a specific problem.
A project consist of a name and a description, the code to execute, the data, and a polyaxonfile.yml.

!!! info "More details"
    Please refer to the [projects section](projects) for more details.

### Experiment Group

An `Experiment Group` is a automatic and practical way to run a version of your model and data with different hyper parameters.

!!! info "More details"
    Please refer to the [experiment groups and hyper parameters search section](experiment_groups) for more details.

### Experiment

An `Experiment` is the execution of your model with data and the provided parameters on the cluster.

!!! info "More details"
    Please refer to the [experiments and distributed runs section](experiments) for more details.

### Job

A `Job` is the Kubernetes pod running on the cluster for a specific experiment,
if an experiment run in a distributed way it will create multiple instances of `Job`.

!!! info "More details"
    Please refer to the [jobs section](jobs) for more details.
