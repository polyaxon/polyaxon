## Get job

```python
get_job(username, project_name, job_id)
```

## Update job

```python
update_job(username, project_name, job_id, patch_dict)
```

## Delete job

```python
delete_job(username, project_name, job_id)
```

## Get job statuses

```python
get_statuses(username, project_name, job_id, page=1)
```

## Restart job

```python
restart(username, project_name, job_id, config=None, update_code=None)
```

## Resume job

```python
resume(username, project_name, job_id, config=None, update_code=None)
```

## Copy job

```python
copy(username, project_name, job_id, config=None, update_code=None)
```

## Stop job

```python
stop(username, project_name, job_id)
```

## Get job resources

```python
resources(username, project_name, job_id, message_handler=None)
```

## Get job logs

```python
logs(username, project_name, job_id, stream=True, message_handler=None)
```

## Download job outputs

```python
download_outputs(username, project_name, job_id)
```
