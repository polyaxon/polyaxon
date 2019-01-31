---
title: "Build Endpoint"
sub_link: "polyaxon-client-python/build-job"
meta_title: "Polyaxon Client Python Build Job Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Build Job Endpoint for creating docker containers."
visibility: public
status: published
tags:
    - client
    - reference
    - polyaxon
    - sdk
    - python
    - build
    - containers
    - docker
sidebar: "polyaxon-client-python"
---

## Get build

```python
polyaxon_client.build_job.get_job(username, project_name, job_id)
```

## Update build

```python
polyaxon_client.build_job.update_job(username, project_name, job_id, patch_dict)
```

## Delete build

```python
polyaxon_client.build_job.delete_job(username, project_name, job_id)
```

## Get build statuses

```python
polyaxon_client.build_job.get_statuses(username, project_name, job_id, page=1)
```

## Stop build

```python
polyaxon_client.build_job.stop(username, project_name, job_id)
```

## Get build logs

```python
polyaxon_client.build_job.logs(
    username,
    project_name,
    job_id,
    stream=True,
    message_handler=print)
```

## Bookmark build

```python
polyaxon_client.build_job.bookmark(username, project_name, job_id)
```

## Unbookmark build

```python
polyaxon_client.build_job.unbookmark(username, project_name, job_id)
```
