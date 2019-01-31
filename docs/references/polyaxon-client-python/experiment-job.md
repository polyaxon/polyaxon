---
title: "Experiment Job Endpoint"
sub_link: "polyaxon-client-python/experiment-job"
meta_title: "Polyaxon Client Python Experiment Job Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Experiment Job Endpoint for tracking the progress of an experiment job."
visibility: public
status: published
tags:
    - client
    - reference
    - polyaxon
    - sdk
    - python
    - logging
    - training
    - experiment
    - job
sidebar: "polyaxon-client-python"
---

## Get experiment job

```python
polyaxon_client.experiment_job.get_job(username, project_name, experiment_id, job_id)
```

## Get experiment job statuses

```python
polyaxon_client.experiment_job.get_statuses(username, project_name, experiment_id, job_id, page=1)
```

## Get experiment job resources

```python
polyaxon_client.experiment_job.resources(
    username,
    project_name,
    experiment_id,
    job_id,
    message_handler=print)
```

## Get experiment job logs

```python
polyaxon_client.experiment_job.logs(
    username,
    project_name,
    experiment_id,
    job_id,
    message_handler=print)
```

