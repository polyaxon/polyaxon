## Get build

```python
polyaxon_clients.build_job.get_job(username, project_name, job_id)
```

## Update build

```python
polyaxon_clients.build_job.update_job(username, project_name, job_id, patch_dict)
```

## Delete build

```python
polyaxon_clients.build_job.delete_job(username, project_name, job_id)
```

## Get build statuses

```python
polyaxon_clients.build_job.get_statuses(username, project_name, job_id, page=1)
```

## Stop build

```python
polyaxon_clients.build_job.stop(username, project_name, job_id)
```

## Get build logs

```python
polyaxon_clients.build_job.logs(
    username,
    project_name,
    job_id,
    stream=True,
    message_handler=print)
```
