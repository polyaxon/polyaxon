---
title: "Tracking experiments reference"
sub_link: "polyaxon-tracking-api/experiments"
meta_title: "Tracking experiments reference - Polyaxon References"
meta_description: "Tracking experiments reference."
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

For tracking experiment running inside a Polyaxon context you can go straight to the [in-cluster section](/references/polyaxon-tracking-api/experiments/in-cluster/). 

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

### create

> Not required for in-cluster experiments

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

### set_name

> Not required for in-cluster experiments

```python
experiment.set_name('new_name')
```

### set_description

> Not required for in-cluster experiments

```python
experiment.set_description('New description ...')
```

### log_tags

> Not required for in-cluster experiments

```python
experiment.log_tags(tags, reset=False)

# Example appending two new tags
experiment.log_tags(['tag1', 'tag2'])

# Example resetting tags
experiment.log_tags('tag3', reset=True)
```

This will merge the new tags with the previous ones if you had tags before, 
otherwise you can reset the tags of the experiment.

### log_framework

> Not required for in-cluster experiments

```python
experiment.log_framework('tensorflow')
```

### log_backend

> Not required for in-cluster experiments

```python
experiment.log_backend('spark')
```

### log_run_env

> Not required for in-cluster experiments

```python
experiment.log_run_env()
```

This step is done automatically when creating an instance with `track_env=True`

### log_code_ref

> Not required for in-cluster experiments

```python
experiment.log_code_ref()
```

This step is done automatically when creating an instance with `track_git=True`


### log_status

> Not required for in-cluster experiments
 
```python
experiment.log_status(status, message=None)

# Example
experiment.log_status('starting')
```

This step is done automatically so this is in general is not needed, because the tracking API will take care of tracking 
the status of your experiment both in-cluster and on other environments.

### log_stopped

> Not required for in-cluster experiments

```python
experiment.log_stopped()
```

This is just an easy way to set a `stopped` status.

### log_succeeded

> Not required for in-cluster experiments

```python
experiment.log_succeeded()
```

This is just an easy way to set a `succeeded` status. 
End of script will trigger succeeded status automatically, 
unless you running a loop and creating a new experiment, 
you need to set the `done` status manually.

### log_failed

> Not required for in-cluster experiments

```python
experiment.log_failed()
```

This is just an easy way to set a `failed` status. Exception will trigger failed status automatically.

### log_metrics

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

### log_params

> Not required for in-cluster experiments

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

### log_data_ref

```python
# Example logging multiple datasets used for the experiment
experiment.log_data_ref(data=dataset1, data_name='my_dataset')
experiment.log_data_ref(data=dataset2, data_name='my_dataset2')

# Example resetting the datasets logged
experiment.log_data_ref(data=dataset3, data_name='my_dataset3', reset=True)
```

### log_artifact

Logs a local file as an artifact and optionally upload it to the registered cloud storage.

```python
experiment.log_artifact(file_path)
```

### log_artifacts

Logs a local directory as artifacts and optionally upload it to the registered cloud storage.

```python
experiment.log_artifacts(dir_path)
```

### get_log_level

Returns the log level defined on the polyaxonfile

### get_outputs_path

Returns the path generated fot this experiment.
