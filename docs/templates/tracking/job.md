Jobs tracking is a high-level API allowing data scientists to track information related to their jobs.

This is only useful for jobs running in a Polyaxon deployment.

## Tracking

```python
from polyaxon_client.tracking import Job

job = Job()
```

### Get job info

Get information about the job.

```python
get_job_info
```

    * project_name
    * job_name
    * project_uuid
    * job_uuid


