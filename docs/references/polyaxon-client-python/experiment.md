---
title: "Experiment Endpoint"
sub_link: "polyaxon-client-python/experiment"
meta_title: "Polyaxon Client Python Experiment Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Experiment Endpoint for creating training, monitoring, and instrumenting experiments."
visibility: public
status: published
tags:
    - client
    - reference
    - polyaxon
    - sdk
    - python
    - tracking
    - instrumentation
    - logging
    - model
    - training
    - experiment
sidebar: "polyaxon-client-python"
---

## Get experiment

```python
polyaxon_client.experiment.get_experiment(username, project_name, experiment_id)
```

## Update experiment

```python
polyaxon_client.experiment.update_experiment(
    username,
    project_name,
    experiment_id,
    patch_dict)
```

## Delete experiment

```python
polyaxon_client.experiment.delete_experiment(username, project_name, experiment_id)
```


## Restart experiment

```python
polyaxon_client.experiment.restart(
    username,
    project_name,
    experiment_id,
    config=None,
    update_code=None)
```

## Resume experiment

```python
polyaxon_client.experiment.resume(
    username,
    project_name,
    experiment_id,
    config=None,
    update_code=None)
```

## Copy experiment

```python
polyaxon_client.experiment.copy(
    username,
    project_name,
    experiment_id,
    config=None,
    update_code=None)
```

## Stop experiment

```python
polyaxon_client.experiment.stop(username, project_name, experiment_id)
```

## Get experiment statuses

```python
polyaxon_client.experiment.get_statuses(
    username,
    project_name,
    experiment_id,
    page=1)
```

## Get experiment metrics

```python
polyaxon_client.experiment.get_metrics(
    username,
    project_name,
    experiment_id,
    page=1)
```

## Create experiment metric

```python
polyaxon_client.experiment.create_metric(
    username,
    project_name,
    experiment_id,
    values)
```

## List experiment jobs

```python
polyaxon_client.experiment.list_jobs(
    username,
    project_name,
    experiment_id,
    page=1)
```

## Get experiment resources

```python
polyaxon_client.experiment.resources(
    username,
    project_name,
    experiment_id,
    message_handler=print)
```

## Get experiment logs

```python
polyaxon_client.experiment.logs(
    username,
    project_name,
    experiment_id,
    stream=True,
    message_handler=print)
```

## Start experiment tensorboard

```python
polyaxon_client.experiment.start_tensorboard(
    username,
    project_name,
    experiment_id,
    job_config=None)
```

## Stop experiment tensorboard

```python
polyaxon_client.experiment.stop_tensorboard(username, project_name, experiment_id)
```

## Download experiment outputs

```python
polyaxon_client.experiment.download_outputs(username, project_name, experiment_id)
```

## Bookmark experiment

```python
polyaxon_client.experiment.bookmark(
    username,
    project_name,
    experiment_id)
```


## Unbookmark experiment

```python
polyaxon_client.experiment.unbookmark(
    username,
    project_name,
    experiment_id)
```
