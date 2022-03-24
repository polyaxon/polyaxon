---
title: "No-op Mode"
sub_link: "python-library/no-op"
meta_title: "Introduction to no-op mode - Python Client References"
meta_description: "Polyaxon's Python library allows to turn off all API calls and silently pass through all function calls."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
sidebar: "core"
---

## Overview

The no-op mode allows users to turn off all API calls and silently pass through all function calls. this behavior is generally useful if a user needs to debug or test
a script without the need to connect to a Polyaxon Cluster.

```bash
export POLYAXON_NO_OP=true
# Or
export POLYAXON_NO_OP="1"
```

or in Python

```python
import os

os.environ["POLYAXON_NO_OP"] = "true"
# Or
os.environ["POLYAXON_NO_OP"] = "1"
```

## Disabling Polyaxon clients without changing code

Since using the Polyaxon client and the tracking API requires code change, e.g.

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient()
run_client = RunClient()
...
# Using the client results in void calls
project_client.list_runs()
project_client.list_versions()
run_client.refresh_data()
run_client.log_inputs(...)
```

Users might need to run the same code outside of a Polyaxon context,
which will break since Polyaxon related operations perform API calls.

Users won't need to perform any change to their code,
they just need to set an environment variable `POLYAXON_NO_OP` to true/1, and the Polyaxon related code will be ignored.
