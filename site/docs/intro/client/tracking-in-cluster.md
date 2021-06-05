---
title: "Tracking in-cluster"
sub_link: "client/tracking-in-cluster"
meta_title: "Introduction to Polyaxon tracking - Python Client References"
meta_description: "Polyaxon's Python library provides utilities and modules for logging and tracking of your machine learning code, artifacts, and results."
visibility: public
status: published
tags:
  - specifications
  - polyaxon
  - python
sidebar: "intro"
---

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

