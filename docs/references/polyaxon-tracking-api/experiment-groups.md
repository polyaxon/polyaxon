---
title: "Tracking API Experiment Groups"
sub_link: "polyaxon-tracking-api/experiment-groups"
meta_title: "Tracking API Experiment Groups - Polyaxon References"
meta_description: "Experiment groups tracking is high level API that allow users to create experiments under one group level. This is very useful for running hyperparameters tuning, and this is how Polyaxon organizes experiments when running hyperparameters tuning."
visibility: public
status: published
tags:
    - tracking
    - reference
    - polyaxon
    - client
    - sdk
    - experiment
    - group
sidebar: "polyaxon-tracking-api"
---

Experiment groups tracking is high level API that allow users to create 
experiments under one group level. This is very useful for running 
hyperparameters tuning, and this is how Polyaxon 
organizes experiments when running hyperparameters tuning.

We thought that in some use cases, the users might want to try some 
algorithms not provided by the platform, to schedule experiment on Polyaxon or to run them on a different platform.

In order to use this API, the user must configure a client

## Creating a group

```python
from polyaxon_client.client import PolyaxonClient

client = PolyaxonClient(host='HOST_IP',
                        token='4ee4e5e6080a196d11f637b950fce1587b29ef36')
```

```python
from polyaxon_client.tracking import Group

group = Group(client=client, project='quick-start')
group.create(tags=['foo', 'bar'], description='New group')
```

## Tracking 

### Starting experiments

```python
experiment = group.create_experiment(tags=tags, description='Some description')
```

This will create an experiment under this group, and provide all context (client api, and storage), to each experiment.

You can then refer to [experiment tracking](/polyaxon_tracking/experiments)


### Log statuses
 
```python
group.log_status(status, message=None)

# Example
group.log_status('starting')
```

### Stop

```python
group.stop()
```

This is just an easy way to set a `stopped` status.

### Succeeded

```python
group.succeeded()
```

This is just an easy way to set a `succeeded` status. End of script will trigger succeeded status automatically

### Failed
```python
group.failed()
```

This is just an easy way to set a `failed` status. Exception will trigger failed status automatically.
