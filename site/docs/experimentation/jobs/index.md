---
title: "Jobs Introduction"
sub_link: "jobs"
is_index: true
meta_title: "Polyaxon Jobs - Experimentation"
meta_description: "A Job is the execution of your model with data and the provided parameters on the cluster."
tags:
  - concepts
  - polyaxon
  - experimentation
  - experiments
  - architecture
sidebar: "experimentation"
---

Jobs are used to train machine learning models,
process a dataset, build container images, execute generic tasks and can be used to perform a variety of functions
from compiling a model to running an ETL operation.

In order to run a job you will need to create a component with a `kind: job` as a runtime:

```yaml
kind: component
version: 1.1
run:
  kind: job
  container:
    image: my-image
    command: [python, model.py]
```

The same example in Python.

```python
from polyaxon.schemas import V1Component, V1Job
from polyaxon import k8s

job = V1Job(
    container=k8s.V1Container(image="my-image", command=["python", "model.py"]),
)

component = V1Component(run=job)
```

### Specification

Please check the [job specification](/docs/experimentation/jobs/specification/) guide to learn about all details for running jobs in Polyaxon.
