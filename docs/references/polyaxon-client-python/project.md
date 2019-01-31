---
title: "Project Endpoint"
sub_link: "polyaxon-client-python/project"
meta_title: "Polyaxon Client Python Project Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Project Endpoint for solving a machine learning, deep learning, data science problem, in collaborative way."
visibility: public
status: published
tags:
    - client
    - reference
    - polyaxon
    - sdk
    - python
    - logging
    - job
sidebar: "polyaxon-client-python"
---

## List projects for user

```python
polyaxon_client.project.list_projects(username, page=1)
```

## Get project

```python
polyaxon_client.project.get_projects(username, project_name)
```

## Create project

```python
polyaxon_client.project.create_project(project_config)
```

## Update project

```python
polyaxon_client.project.update_project(username, project_name, patch_dict)
```

## Delete project

```python
polyaxon_client.project.delete_project(username, project_name)
```

## Upload repo for a project

```python
polyaxon_client.project.upload_repo(
    username,
    project_name,
    files,
    files_size=None)
```

## Download repo for a project

```python
polyaxon_client.project.download_repo(username, project_name)
```

## List experiment groups

```python
polyaxon_client.project.list_experiment_groups(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Create experiment groups

```python
polyaxon_client.project.create_experiment_group(
    username,
    project_name,
    experiment_group_config)
```

## List experiments

```python
polyaxon_client.project.list_experiments(
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
polyaxon_client.project.create_experiment(
    username,
    project_name,
    experiment_config)
```

## List Jobs

```python
polyaxon_client.project.list_jobs(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Create Job

```python
polyaxon_client.project.create_job(
    username,
    project_name,
    job_config)
```

## List Builds

```python
polyaxon_client.project.list_builds(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Create Build

```python
polyaxon_client.project.create_build(
    username,
    project_name,
    build_config)
```


## List tensorboards

```python
polyaxon_client.project.list_tensorboards(
    username,
    project_name,
    query=None,
    sort=None,
    page=1)
```

## Start project tensorboard

```python
polyaxon_client.project.start_tensorboard(
    username,
    project_name,
    job_config)
```

## Stop project tensorboard

```python
polyaxon_client.project.stop_tensorboard(username, project_name)
```

## Start notebook

```python
polyaxon_client.project.start_notebook(
    username,
    project_name,
    job_config)
```

## Stop notebook

```python
polyaxon_client.project.stop_notebook(username, project_name, commit=True)
```

## Bookmark notebook

```python
polyaxon_client.project.bookmark(username, project_name)
```

## Unbookmark notebook

```python
polyaxon_client.project.unbookmark(username, project_name)
```
