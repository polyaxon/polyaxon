---
title: "No-op Mode"
sub_link: "tracking/no-op"
meta_title: "Introduction to no-op mode - Tracking - Experimentation"
meta_description: "Polyaxon's Python library allows to turn off all API calls and silently pass through all function calls."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
  - tracking
  - reference
  - sdk
sidebar: "experimentation"
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

## Disabling tracking without changing code

Since using the tracking API requires code change, e.g.

```python
from polyaxon.tracking import Run

# Polyaxon experiment
experiment = Run()
# training code ...
# Metrics reporting
experiment.log_metrics(step=1000, loss=0.01, accuracy=0.97)
```

Users might need to run the same code outside of a Polyaxon context,
which will break since Polyaxon related operations perform API calls.

Users won't need to perform any change to their code,
they just need to set an environment variable `POLYAXON_NO_OP` to true/1, and the Polyaxon related code will be ignored.
