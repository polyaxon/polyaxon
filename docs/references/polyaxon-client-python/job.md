---
title: "Job Endpoint"
sub_link: "polyaxon-client-python/job"
meta_title: "Polyaxon Client Python Job Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Job Endpoint for preparing data, preprocessing data, augmenting data, feature engineering jobs."
visibility: public
status: published
tags:
    - client
    - specifications
    - polyaxon
    - sdk
    - python
    - logging
    - job
sidebar: "polyaxon-client-python"
---

## Get job

```python
polyaxon_client.job.get_job(username, project_name, job_id)
```

## Update job

```python
polyaxon_client.job.update_job(username, project_name, job_id, patch_dict)
```

## Delete job

```python
polyaxon_client.job.delete_job(username, project_name, job_id)
```

## Get job statuses

```python
polyaxon_client.job.get_statuses(username, project_name, job_id, page=1)
```

## Restart job

```python
polyaxon_client.job.restart(username, project_name, job_id, config=None, update_code=None)
```

## Resume job

```python
polyaxon_client.job.resume(username, project_name, job_id, config=None, update_code=None)
```

## Copy job

```python
polyaxon_client.job.copy(username, project_name, job_id, config=None, update_code=None)
```

## Stop job

```python
polyaxon_client.job.stop(username, project_name, job_id)
```

## Get job resources

```python
polyaxon_client.job.resources(username, project_name, job_id, message_handler=None)
```

## Get job logs

```python
polyaxon_client.job.logs(username, project_name, job_id, stream=True, message_handler=None)
```

## Download job outputs

```python
polyaxon_client.job.download_outputs(username, project_name, job_id)
```

## Bookmark job

```python
polyaxon_client.job.bookmark(username, project_name, job_id)
```

## Unbookmark job

```python
polyaxon_client.job.unbookmark(username, project_name, job_id)
```
