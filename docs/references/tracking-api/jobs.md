---
title: "Tracking API Jobs"
sub_link: "tracking-api/jobs"
meta_title: "Tracking API Jobs - Polyaxon References"
meta_description: "Jobs tracking is a high-level API allowing data scientists to track information related to their jobs."
visibility: public
status: published
tags:
    - tracking
    - reference
    - polyaxon
    - client
    - sdk
    - job
sidebar: "tracking-api"
---

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


