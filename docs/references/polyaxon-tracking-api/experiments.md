---
title: "Tracking API Experiments"
sub_link: "polyaxon-tracking-api/experiments"
meta_title: "Tracking API Experiments - Polyaxon References"
meta_description: "Experiments tracking is a high-level API allowing data scientists to track information related to their experiments."
visibility: public
status: published
tags:
    - tracking
    - reference
    - polyaxon
    - client
    - sdk
    - experiment
sidebar: "polyaxon-tracking-api"
---

Experiments tracking is a high-level API allowing data scientists to track information related to their experiments.

For tracking experiment running inside a Polyaxon context you can go straight to this [section](/references/polyaxon-tracking-api/experiments/#tracking-experiments-running-inside-polyaxon).

## Tracking

When a user creates an `Experiment` instance, the instance will automatically log 
code reference, command and arguments used, the run environment, and much more.
 
Optionally the user can log as well hyper parameters, data reference, metrics, and model outputs.

You can create an `Experiment` instance this way:

```python
from polyaxon_client.tracking import Experiment

experiment = Experiment(
    project=None,
    experiment_id=None,
    group_id=None,
    client=None,
    track_logs=True,
    track_git=True,
    track_env=True,
    outputs_store=None)
```

When a user creates an `Experiment` instance, 
it either detects an existing experiment and the tracking api will request additional information about it,
or create the needed information to start a new one.

We will get back to this optional parameters in following sections with use cases and examples.
But before we do that, let's look at what the user can do with and `Experiment` instance.

### Starting an experiment

```python
# Example created with tags and description 
experiment.create(tags=['tensorflow', 'nlp'], description='My first Polyaxon experiment')

# Example created with a name (must be a slug)
experiment.create(name='experiment_name')
```

This will start an experiment with tags and description, this information is not required, 
and you can start an experiment with no information:

```python
experiment.create()
```

You can update the information later if you want.

### Update the name

```python
experiment.set_name('new_name')
```

### Update the description

```python
experiment.set_description('New description ...')
```

### Log tags

```python
experiment.log_tags(tags, reset=False)

# Example appending two new tags
experiment.log_tags(['tag1', 'tag2'])

# Example resetting tags
experiment.log_tags('tag3', reset=True)
```

This will merge the new tags with the previous ones if you had tags before, 
otherwise you can reset the tags of the experiment.

### Log run environment

```python
experiment.log_run_env()
```

This step is done automatically when creating an instance with `track_env=True`

### Log code reference 

```python
experiment.log_code_ref()
```

This step is done automatically when creating an instance with `track_git=True`


### Log statuses
 
```python
experiment.log_status(status, message=None)

# Example
experiment.log_status('starting')
```

This step is done automatically so this is in general is not needed, because the tracking API will take care of tracking 
the status of your experiment both in-cluster and on other environments.

### Stop

```python
experiment.stop()
```

This is just an easy way to set a `stopped` status.

### Succeeded

```python
experiment.succeeded()
```

This is just an easy way to set a `succeeded` status. 
End of script will trigger succeeded status automatically, 
unless you running a loop and creating a new experiment, 
you need to set the `done` status manually.

### Failed

```python
experiment.failed()
```

This is just an easy way to set a `failed` status. Exception will trigger failed status automatically.

### Log metrics

```python
experiment.log_metrics(step=123, loss=0.023, accuracy=0.91)
```

It's very important to log `step` as one of your metrics if you want to compare experiments on the dashboard 
and use the steps in x-axis instead of timestamps.

!!! tip "Add a `step` as one of the metrics you track for the metrics' dashboards"
    Polyaxon provides custom metrics charting and dashboards. 
    In many instance it's useful to compare experiments, this could be challenging for 
    experiments ran sequentially, since the x-axis will use by default timestamps, 
    if your experiments report steps as well you can switch the series to use steps instead of timestamps.

### Log params

```python
# Example logging params
experiment.log_params(activation='sigmoid', lr=0.001)

# Example appending more params
experiment.log_params(dropout=0.5)

# Example logging and resetting params
experiment.log_params(activation='sigmoid', learning_rate=0.001, reset=True)
```

Logging params for experiments in-cluster is generally handled through the `polyaxonfile` with the declaration section. 
But often times, users might need to update or add more params during the experiment run.

### Log data references

```python
# Example logging multiple datasets used for the experiment
experiment.log_data_ref(data=dataset1, data_name='my_dataset')
experiment.log_data_ref(data=dataset2, data_name='my_dataset2')

# Example resetting the datasets logged
experiment.log_data_ref(data=dataset3, data_name='my_dataset3', reset=True)
```

## Tracking experiments running inside Polyaxon

For experiment running and managed by Polyaxon, an in-cluster context is exposed to the tracking API 
to transparently detect the experiment context, project, 
experiment group if the experiment belongs to a group, authentication, outputs paths, logs paths, and storage definition.

The only step needed is to create an instance of `Experiment`:

```python
from polyaxon_client.tracking import Experiment

experiment = Experiment()
...
experiment.log_metrics(step=1000, loss=0.01, accuracy=0.97)
```

Since hyperparams are defined in the `declarations` section of the Polyaxonfile, 
you generally don't need to  

You can access this context using the following methods:

 * `experiment.get_cluster_def`: Returns cluster definition created by polyaxon, 
 this value is also exposed as an env var `POLYAXON_CLUSTER`.
    ```json
    {
        "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000",
                   "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "ps": ["plxjob-ps3-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
    }
    ```
 * `experiment.get_declarations`: Returns all the experiment declarations based on both, 
 this value is also exposed as an env var `POLYAXON_DECLARATIONS`.

    * declarations section
    * matrix section

 * `experiment.get_tf_config`: Returns the TF_CONFIG defining the cluster and the current task, 
    if the experiment is running a distributed tensorflow graph.
    if `envvar` is not null, it will set and env variable with `envvar`.

 * `experiment.get_experiment_info`: Returns information about the experiment, 
 this value is also exposed as an env var `POLYAXON_EXPERIMENT_INFO`.

    * project_name
    * experiment_group_name
    * experiment_name
    * project_uuid
    * experiment_group_uuid
    * experiment_uuid

 * `experiment.get_task_info`: Returns the task info: `{"type": str, "index": int}`, 
 this value is also exposed as an env var `POLYAXON_TASK_INFO`.


### Accessing the API

Since the experiment is running in-cluster, the tracking API knows how to instantiate a client, 
this client is used not only to log the previous information, 
but it could be used to access to much richer API.

```python
client = experiment.client
```

This client is authenticated with the current user, and gives scoped access to all accessible objects of the user.

Please look at [Polyaxon client](/polyaxon_client/introduction) for more information.

## Tracking experiments running outside Polyaxon

In order to track experiment running outside of Polyaxon, the user must configure a client.

```python
from polyaxon_client.client import PolyaxonClient

client = PolyaxonClient(host='HOST_IP',
                        token='4ee4e5e6080a196d11f637b950fce1587b29ef36')
```

The user must provide information about the experiment, the project where this experiment should be added.

```python
# An experiment in a project that belongs to the authenticated user 
experiment = Experiment(client=client, project='quick-start')

# An experiment in a project that belongs to another user 
# The authenticated user must have access rights to the project 
experiment = Experiment(client=client, project='user2/t2t')
```

You can use the client to create a project as well, and then create an experiment.

```python
project = client.project.create_project({name: 'new_project', 'description': 'some decription', tags: ...})
```

