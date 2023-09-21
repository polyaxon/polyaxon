---
title: "Tracking in-cluster"
sub_link: "tracking/in-cluster"
meta_title: "Introduction to Polyaxon tracking - Tracking - Experimentation"
meta_description: "Polyaxon's tracking provides utilities and modules for logging and tracking of your machine learning code, artifacts, and results."
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

When calling tracking module in-cluster, Polyaxon performs a couple of checks to automatically load a context defined by the scheduler.
Additionally, this context contains a scoped token to communicate with the API to only authorize the job or service to perform requests to accessible entities only.

## In-cluster tracking

If you are running an experiment in-cluster:

```python

from random import random, randint

from polyaxon.schemas import V1ArtifactKind
from polyaxon import tracking

if __name__ == "__main__":
    # No need to specify anything, a context is provided in-cluster
    tracking.init()

    # Log additional parameter
    tracking.log_inputs(param1=randint(0, 100))

    # Log additional tags
    tracking.log_tags(["foo", "bar"])

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

