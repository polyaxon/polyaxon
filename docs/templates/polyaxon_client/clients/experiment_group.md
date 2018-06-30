## Get experiment group

```python
polyaxon_clients.experiment_group.get_experiment_group(username, project_name, group_id)
```

## List experiment group experiments

```python
polyaxon_clients.experiment_group.list_experiments(
    username,
    project_name,
    group_id,
    metrics=None,
    declarations=None,
    query=None,
    sort=None,
    page=1)
```

## Update experiment group

```python
polyaxon_clients.experiment_group.update_experiment_group(
    username,
    project_name,
    group_id,
    patch_dict)
```

## Delete experiment group

```python
polyaxon_clients.experiment_group.delete_experiment_group(username, project_name, group_id)
```

## Stop experiment group

```python
polyaxon_clients.experiment_group.stop(username, project_name, group_id, pending=False)
```

## Start experiment group tensorboard

```python
polyaxon_clients.experiment_group.start_tensorboard(
    username,
    project_name,
    group_id,
    job_config=None)
```

## Stop experiment group tensorboard

```python
polyaxon_clients.experiment_group.stop_tensorboard(username, project_name, group_id)
```
