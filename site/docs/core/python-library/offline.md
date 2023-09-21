---
title: "Tracking offline"
sub_link: "python-library/tracking-offline"
meta_title: "Introduction to Polyaxon tracking offline - Python Client References"
meta_description: "Polyaxon's Python library enables users to perform all API calls and artifacts tracking logic offline."
visibility: public
status: published
tags:
  - specifications
  - polyaxon
  - python
sidebar: "core"
---

## Overview

The offline mode allows users to use the RunClient or to connect to an offline run persisted on a local path, outside of a Polyaxon cluster.
When the offline mode is enabled , Polyaxon will perform all API and tracking related code locally without needing access to a Polyaxon API, and will persist any generated artifacts or API blobs locally.

## Setting the offline mode

To configure the offline mode using the environment variable, users just need to set an environment variable `POLYAXON_IS_OFFLINE` to true/1.

```bash
export POLYAXON_IS_OFFLINE=true
# Or
export POLYAXON_IS_OFFLINE="1"
```

or in Python

```python
import os

os.environ["POLYAXON_IS_OFFLINE"] = "true"
# Or
os.environ["POLYAXON_IS_OFFLINE"] = "1"
```

It's also possible to set the offline mode using the client directly:

```python
from polyaxon.client import RunClient

...
run_client = RunClient(..., is_offline=True, ...)
...
run_client.log_inputs(foo="bar", key="value", param=2.3)
run_client.log_outputs(result1=11, result2="foo")
...
print(run_client.run_uuid)
print(run_client.run_data)
...
run_client.persist_run(path="/tmp/offline/")
```

## Resuming an offline run

If you are running outside of a Polyaxon cluster and you need to resume an offline run:

```python
from polyaxon.client import RunClient

# Resume run
run_client = RunClient.load_offline_run(path="/tmp/offline", raise_if_not_found=True)
...
print(run_client.run_uuid)
print(run_client.run_data)
...
```
