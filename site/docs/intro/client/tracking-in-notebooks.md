---
title: "Tracking in Notebooks"
sub_link: "client/tracking-in-notebooks"
meta_title: "Introduction to Polyaxon tracking in a notebook session- Python Client References"
meta_description: "Polyaxon's Python library provides utilities and modules for logging and tracking of your machine learning code, artifacts, and results, and allows to perform multi-run tracking inside a single notebook session."
visibility: public
status: published
is_index: true
tags:
  - specifications
  - polyaxon
  - python
sidebar: "intro"
---

## In-cluster tracking in a notebook session

Polyaxon's Python library provides utilities and modules for logging and tracking of your machine learning code, artifacts, 
and results, and allows to perform multi-run tracking inside a single notebook session.

If you are running an notebook in-cluster, and you need to track some experiments running inside the notebook, you need to start and end the experiments manually:

```python
from polyaxon import tracking

# Start run1
tracking.init(name="run1", is_new=True)

# ...

# End run1
tracking.end()

# ...

# Start run2
tracking.init(name="run2", is_new=True)

# ...

# End run2
tracking.end()
```
