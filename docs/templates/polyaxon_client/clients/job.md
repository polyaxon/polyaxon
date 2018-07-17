## Get job

```python
polyaxon_clients.job.get_job(username, project_name, job_id)
```

## Update job

```python
polyaxon_clients.job.update_job(username, project_name, job_id, patch_dict)
```

## Delete job

```python
polyaxon_clients.job.delete_job(username, project_name, job_id)
```

## Get job statuses

```python
polyaxon_clients.job.get_statuses(username, project_name, job_id, page=1)
```

## Restart job

```python
polyaxon_clients.job.restart(username, project_name, job_id, config=None, update_code=None)
```

## Resume job

```python
polyaxon_clients.job.resume(username, project_name, job_id, config=None, update_code=None)
```

## Copy job

```python
polyaxon_clients.job.copy(username, project_name, job_id, config=None, update_code=None)
```

## Stop job

```python
polyaxon_clients.job.stop(username, project_name, job_id)
```

## Get job resources

```python
polyaxon_clients.job.resources(username, project_name, job_id, message_handler=None)
```

## Get job logs

```python
polyaxon_clients.job.logs(username, project_name, job_id, stream=True, message_handler=None)
```

## Download job outputs

```python
polyaxon_clients.job.download_outputs(username, project_name, job_id)
```

## Bookmark job

```python
polyaxon_clients.job.bookmark(username, project_name, job_id)
```

## Unbookmark job

```python
polyaxon_clients.job.unbookmark(username, project_name, job_id)
```
