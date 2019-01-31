---
title: "Experiment Group Endpoint"
sub_link: "polyaxon-client-python/experiment-group"
meta_title: "Polyaxon Client Python Experiment Group Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Experiment Group Endpoint for creating, optimizing, and searching large hyperparameters search space."
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
    - hyperparameters
    - optimization
    - tuning
    - search
    - group
    - model
    - training
    - experiment
sidebar: "polyaxon-client-python"
---

## Get experiment group

```python
polyaxon_client.experiment_group.get_experiment_group(username, project_name, group_id)
```

## List experiment group experiments

```python
polyaxon_client.experiment_group.list_experiments(
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
polyaxon_client.experiment_group.update_experiment_group(
    username,
    project_name,
    group_id,
    patch_dict)
```

## Delete experiment group

```python
polyaxon_client.experiment_group.delete_experiment_group(username, project_name, group_id)
```

## Stop experiment group

```python
polyaxon_client.experiment_group.stop(username, project_name, group_id, pending=False)
```

## Get experiment group statuses

```python
polyaxon_client.experiment_group.get_statuses(username, project_name, group_id)
```

## Start experiment group tensorboard

```python
polyaxon_client.experiment_group.start_tensorboard(
    username,
    project_name,
    group_id,
    job_config=None)
```

## Stop experiment group tensorboard

```python
polyaxon_client.experiment_group.stop_tensorboard(username, project_name, group_id)
```

## Bookmark experiment group

```python
polyaxon_client.experiment_group.bookmark(username, project_name, group_id)
```

## Unbookmark experiment group

```python
polyaxon_client.experiment_group.unbookmark(username, project_name, group_id)
```
