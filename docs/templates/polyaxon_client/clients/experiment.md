## Get experiment

```python
get_experiment(username, project_name, experiment_id)
```

## Update experiment

```python
polyaxon_clients.experiment.update_experiment(
    username,
    project_name,
    experiment_id,
    patch_dict)
```

## Delete experiment

```python
polyaxon_clients.experiment.delete_experiment(username, project_name, experiment_id)
```

## Get experiment statuses

```python
polyaxon_clients.experiment.get_statuses(
    username,
    project_name,
    experiment_id,
    page=1)
```

## Get experiment metrics

```python
polyaxon_clients.experiment.get_metrics(
    username,
    project_name,
    experiment_id,
    page=1)
```

## Create experiment metric

```python
polyaxon_clients.experiment.create_metric(
    username,
    project_name,
    experiment_id,
    values)
```

## List experiment jobs

```python
polyaxon_clients.experiment.list_jobs(
    username,
    project_name,
    experiment_id,
    page=1)
```

## Restart experiment

```python
polyaxon_clients.experiment.restart(
    username,
    project_name,
    experiment_id,
    config=None,
    update_code=None)
```

## Resume experiment

```python
polyaxon_clients.experiment.resume(
    username,
    project_name,
    experiment_id,
    config=None,
    update_code=None)
```

## Copy experiment

```python
polyaxon_clients.experiment.copy(
    username,
    project_name,
    experiment_id,
    config=None,
    update_code=None)
```

## Stop experiment

```python
polyaxon_clients.experiment.stop(username, project_name, experiment_id)
```

## Get experiment resources

```python
polyaxon_clients.experiment.resources(
    username,
    project_name,
    experiment_id,
    message_handler=print)
```

## Get experiment logs

```python
polyaxon_clients.experiment.logs(
    username,
    project_name,
    experiment_id,
    stream=True,
    message_handler=print)
```

## Start experiment tensorboard

```python
polyaxon_clients.experiment.start_tensorboard(
    username,
    project_name,
    experiment_id,
    job_config=None)
```

## Stop experiment tensorboard

```python
polyaxon_clients.experiment.stop_tensorboard(username, project_name, experiment_id)
```

## Download experiment outputs

```python
polyaxon_clients.experiment.download_outputs(username, project_name, experiment_id)
```
