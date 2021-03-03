---
title: "Quick Start"
sub_link: "tracking/quick-start"
meta_title: "Enable tracking for your machine learning code - Tracking - Experimentation"
meta_description: "Enable tracking for your machine learning code."
visibility: public
status: published
tags:
  - tracking
  - reference
  - polyaxon
  - client
  - sdk
sidebar: "experimentation"
---

Polyaxon provides feature complete tracking and dashboarding capabilities for your ML scripts.  

## In-cluster tracking

If you are running an experiment in-cluster:

```python

from random import random, randint

from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon import tracking

if __name__ == "__main__":
    # No need to specify anything, a context is provided in-cluster
    tracking.init()

    # Log additional parameter
    tracking.log_inputs(param1=randint(0, 100))

    # Log a single metric
    tracking.log_metric(name="metric1", value=random(), step=OPTIONAL, timestamp=OPTIONAL)
    # Log multiple metrics at once
    tracking.log_metrics(metric2=random(), metric3=random(), step=OPTIONAL, timestamp=OPTIONAL)
    
    # Log a final results
    tracking.log_outputs(res1=randint(0, 100), res2="test value", ...) 

    # Save the artifact
    asset_path = tracking.get_outputs_path("test.txt")
    with open(asset_path, "w") as f:
        f.write("Artifact content.")
    # Track the lineage Name will default to test
    tracking.log_artifact_ref(path=asset_path, kind=V1ArtifactKind.FILE)
    
    # Save a second artifact 
    asset_path = tracking.get_outputs_path("file.csv")
    with open(asset_path, "w") as f:
        f.write("Artifact content.")
    # Track the with a different name
    tracking.log_artifact_ref(path=asset_path, kind=V1ArtifactKind.CSV, name="my-csv")
```


## In-cluster tracking inside a notebook

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

## Out of a Polyaxon cluster offline tracking

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

## Out of a Polyaxon cluster multiple offline tracking

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
