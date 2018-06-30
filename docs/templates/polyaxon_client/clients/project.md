## List projects for user

```python
polyaxon_clients.project.list_projects(username, page=1)
```

## Get project

```python
polyaxon_clients.project.get_projects(username, project_name)
```

## Create project

```python
polyaxon_clients.project.create_project(project_config)
```

## Update project

```python
polyaxon_clients.project.update_project(username, project_name, patch_dict)
```

## Delete project

```python
polyaxon_clients.project.delete_project(username, project_name)
```

## Upload repo for a project

```python
polyaxon_clients.project.upload_repo(
    username,
    project_name,
    files,
    files_size=None)
```

## Download repo for a project

```python
polyaxon_clients.project.download_repo(username, project_name)
```

## List experiment groups

```python
polyaxon_clients.project.list_experiment_groups(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Create experiment groups

```python
polyaxon_clients.project.create_experiment_group(
    username,
    project_name,
    experiment_group_config)
```

## List experiments

```python
polyaxon_clients.project.list_experiments(
    username,
    project_name,
    independent=None,
    group=None,
    metrics=None,
    declarations=None,
    query=None,
    sort=None,
    page=1)
```

## Create experiment

```python
polyaxon_clients.project.create_experiment(
    username,
    project_name,
    experiment_config)
```

## List Jobs

```python
polyaxon_clients.project.list_jobs(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Create Job

```python
polyaxon_clients.project.create_job(
    username,
    project_name,
    job_config)
```

## List Builds

```python
polyaxon_clients.project.list_builds(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Create Build

```python
polyaxon_clients.project.create_build(
    username,
    project_name,
    build_config)
```


## List tensorboards

```python
polyaxon_clients.project.list_tensorboards(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Start project tensorboard

```python
polyaxon_clients.project.start_tensorboard(
    username,
    project_name,
    job_config)
```

## Stop project tensorboard

```python
polyaxon_clients.project.stop_tensorboard(username, project_name)
```

## Start notebook

```python
polyaxon_clients.project.start_notebook(
    username,
    project_name,
    job_config)
```

## Stop notebook

```python
polyaxon_clients.project.stop_notebook(username, project_name, commit=True)
```
