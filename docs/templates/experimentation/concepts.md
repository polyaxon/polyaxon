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
it provides the user a wide range of possibilities to [customize the run environment](/customization/customize_run_environment)
to fit the requirements and dependencies needed for the experiments.

![architecture](/images/polyaxon_architecture.png)


## Concepts

Polyaxon relies on a set of concepts to manage an experimentation workflow,
in this section we provide a high level introduction to these concepts,
with more details in pages dedicated to each concept.


### User

A `User` is the entity that creates projects, starts experiments, manages teams and clusters.
A `User` has a set of permissions, and can be normal user or superuser.

!!! info "More details"
    Please refer to the [management section](/management/introduction) for more details.

### Teams

An `Team` provides a way to manage team/group of users, their access roles, and resources quotas.

!!! caution
    This is still a work in progress.
    If you want to be notified when we release this feature, please [subscribe](https://polyaxon.com/signup/) to receive our progress.


### Project

A `Project` in Polyaxon is very similar to a project in github,
it aims at organizing your efforts to solve a specific problem.
A project consist of a name and a description, the code to execute, the data, and a polyaxonfile.yml.

!!! info "More details"
    Please refer to the [projects section](projects) for more details.


### Experiment Group

An `Experiment Group` is an automatic and practical way to run a version of your model and data with different hyper parameters.

!!! info "More details"
    Please refer to the [experiment groups and hyper parameters search section](experiment_groups) for more details.


### Experiment

An `Experiment` is the execution of your model with data and the provided parameters on the cluster.

!!! info "More details"
    Please refer to the [experiments and distributed runs section](experiments) for more details.


### Experiment Job

A `Experiment Job` is the Kubernetes pod running on the cluster for a specific experiment,
if an experiment run in a distributed way it will create multiple instances of `Experiment Job`.

!!! info "More details"
    Please refer to the [experiment jobs section](experiment_jobs) for more details.


### Distributed Experiments

A `Distributed Experiment` is the execution of a model or a computation graph across a cluster.

!!! info "More details"
    Please refer to the [distributed experiments](distributed_experiments) for more details.


### Job

A `Job` is the execution of your your code to do some data processing or any generic operation.

!!! info "More details"
    Please refer to the [jobs section](jobs) for more details.


### Hyperparameters search

Finding good hyperparameters involves can be very challenging,
and requires to efficiently search the space of possible hyperparameters as well as
how to manage a large set of experiments for hyperparameter tuning.

!!! info "More details"
    Please refer to the [hyperparameters search](hyperparameters_search) for more details.


### Checkpointing, resuming and restarting experiments

Checkpointing is a very important concept in machine learning, it prevents losing progress.
It also provide the possibility to resume an experiment from a specific state.

Polyaxon provides some structure and organization regarding checkpointing and outputs saving.


!!! info "More details"
    Please refer to the [save, resume & restart](save_resume_restart) for more details.


### Tensorboard

A `Tensorboard` is a job running to visualize the metrics of an experiment,
the experiments of a group, or of a project.

!!! info "More details"
    Please refer to the [tensorboard](tensorboard) for more details.

### Notebooks

A `Project plugin` is a job running project wide. Currently, Polyaxon offers 2 plugins: Tensorboard and Jupyter notebook.

!!! info "More details"
    Please refer to the [project plugins section](project_plugins) for more details.
