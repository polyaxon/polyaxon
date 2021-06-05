---
title: "Tracking offline"
sub_link: "client/tracking-offline"
meta_title: "Introduction to Polyaxon tracking offline - Python Client References"
meta_description: "Polyaxon's Python library enables users to perform all API calls and artifacts tracking logic offline."
visibility: public
status: published
tags:
  - specifications
  - polyaxon
  - python
sidebar: "intro"
---

## Overview

The offline mode allows users to track or to resume an offline run, outside of a Polyaxon cluster.
When the offline mode is enabled , Polyaxon will perform all API and tracking related code locally without needing access to a Polyaxon API, and will persist any generated artifacts or API blobs locally.

## Setting the offline mode

To configure the offline mode using the environment variable, users just need to set an environment variable `POLYAXON_IS_OFFLINE` to true/1.
It's also possible to set the offline mode using the tracking `Run(..., is_offline=True, ...)` class or the tracking `tracking.init(..., is_offline=True, ...)` module. 

## Offline tracking

If you are running outside of a Polyaxon cluster (non-managed runs):

```python
from polyaxon import tracking

if __name__ == "__main__":
    # Getting the project from the local cache, otherwise it will raise
    tracking.init(is_offline=True)
    
    ...
```

Providing the project manually:

```python
from polyaxon import tracking

if __name__ == "__main__":
    tracking.init(project="owner/project", name="run1", is_offline=True)
    
    ...
```

## Tracking multiple offline runs

If you are running outside of a Polyaxon cluster and you need to track multiple runs:

```python
from polyaxon import tracking

# Start run1
tracking.init(name="run1", is_new=True, is_offline=True)

# ...

# End run1
tracking.end()

# ...

# Start run2
tracking.init(project="owner/project2", name="run2", is_new=True, is_offline=True)

# ...

# End run2
tracking.end()
```

## Resuming an offline run

If you are running outside of a Polyaxon cluster and you need to resume an offline run:

```python
from polyaxon import tracking

# Resume run
tracking.init(run_uuid="UUID_OF_THE_PREVIOUS_OFFLINE_RUN")

# ...
```
