---
title: "Tracking in Notebooks"
sub_link: "tracking/in-notebooks"
meta_title: "Introduction to Polyaxon tracking in a notebook session - Tracking - Experimentation"
meta_description: "Polyaxon's Python library provides utilities and modules for logging and tracking of your machine learning code, artifacts, and results, and allows to perform multi-run tracking inside a single notebook session."
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
  - notebook
sidebar: "experimentation"
---

## Tracking in a notebook session

Polyaxon's Python library provides utilities and modules for logging and tracking of your machine learning code, artifacts, 
and results, and allows to perform multi-run tracking inside a single notebook session.

If you need to track some experiments running inside a notebook, you need to start and end the experiments manually:

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

If you are running the notebook [in-cluster](/docs/experimentation/tracking/in-cluster/), you do not need to provide the authentication and owner/project context because it will be resolved automatically using the same notebook session.

If you the notebook is running outside of Polyaxon or managed manually, you might need to provide the context manually, see the [instantiation guide](/docs/experimentation/tracking/instantiation/) for more details.
