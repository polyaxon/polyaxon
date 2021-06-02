---
title: "No-op Mode"
sub_link: "client/no-op"
meta_title: "Introduction to no-op mode - Python Client References"
meta_description: "Polyaxon's Python library allows to turn off all API calls and silently pass through all function calls."
visibility: public
status: published
is_index: true
tags:
  - specifications
  - polyaxon
  - python
sidebar: "intro"
---

## Overview

The no-op mode allows users to turn off all API calls and silently pass through all function calls. this behavior is generally useful if a user needs to debug or test
a script without the need to connect to a Polyaxon Cluster. 

## Disabling Polyaxon clients without changing the code

Since using the Polyaxon client and the tracking API requires code change, e.g.

```python
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
