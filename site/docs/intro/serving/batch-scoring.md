---
title: "Batch scoring"
sub_link: "serving/batch-scoring"
meta_title: "Batch scoring - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Batch scoring - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - notebook
  - quick-start
sidebar: "intro"
---

## Overview

In the previous guide we trained several models. In this section we will demonstrate how to deploy a batch scoring job.
This type of jobs can be used for batch inference or data processing workloads,
it can be used also for running ML models using a variety of frameworks such as: PyTorch, ONNX, scikit-learn, XGBoost, TensorFlow (if not using SavedModels), etc.

All code and manifests used in this tutorial can be found in this [github repo](https://github.com/polyaxon/polyaxon-ml-serving).

## Logged model

In our training script we used Polyaxon to log a model every time we run an experiment:

```python
# Logging the model
tracking.log_model(model_path, name="iris-model", framework="scikit-learn", versioned=False)
```

> **Note**: the `versioned` was removed in version `>v1.17` and is the default behavior.

## Deploying a batch job

We will deploy a simple job that will load the best model based on accuracy as and run a scoring logic on a dataset loaded from a CSV file.
In order to make this example simple and runnable, we decided to host the CSV file directly on the repo, however the provenance of the dataset can be an S3/GCS bucket, a URL, or mounted path.
The job itself expects a csv filepath and a model path, which can be exposed on the job component as well.


```python
import argparse

import joblib
import pandas as pd

from polyaxon import tracking
from polyaxon.schemas import V1ArtifactKind

IRIS_CLASS_MAPPING = {0: "setosa", 1: "versicolor", 2: "virginica"}


def load_model(model_path: str):
    model = open(model_path, "rb")
    return joblib.load(model)


def load_dataset(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def score(data: pd.DataFrame) -> pd.DataFrame:
    feature_columns = ["sepal.length", "sepal.width", "petal.length", "petal.width"]
    data['prediction'] = classifier.predict(data[feature_columns].values)
    data['prediction_class'] = (data['prediction'].apply(lambda i: IRIS_CLASS_MAPPING[i]))

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model-path',
        type=str,
        default="./model.joblib",
    )
    parser.add_argument(
        '--csv-path',
        type=str,
        default="./inputs.csv",
    )
    args = parser.parse_args()

    tracking.init()

    classifier = load_model(args.model_path)
    print("Started scoring csv {}!".format(args.csv_path))
    data = load_dataset(args.csv_path)
    scores = score(data)

    results_path = tracking.get_outputs_path("results.csv")
    scores.to_csv(results_path, index=False)
    tracking.log_artifact_ref(
        results_path,
        name="scoring-results",
        is_input=False,
        kind=V1ArtifactKind.CSV,
    )
    print("Finished scoring!")
```

The custom component has a single input, it expects a run uuid, it then loads the model and copy it under the path `polyaxon-ml-serving/batch-scoring/model.joblib`.

```yaml
version: 1.1
kind: component
name: batch-scoring
tags: ["scoring", "job"]

inputs:
- name: uuid
  type: str

run:
  kind: job
  init:
  - git: {"url": "https://github.com/polyaxon/polyaxon-ml-serving"}
  - artifacts: {"files": [["{{ uuid }}/outputs/model/model.joblib", "{{ globals.artifacts_path }}/polyaxon-ml-serving/batch-scoring/model.joblib"]]}
  container:
    image: polyaxon/polyaxon-examples:ml-serving
    workingDir: "{{ globals.artifacts_path }}/polyaxon-ml-serving/batch-scoring"
    command: ["python", "-u", "scoring_job.py"]
```

To schedule the job with Polyaxon:

```bash
polyaxon run -f batch-scoring/polyaxonfile.yaml -P uuid=f8176c9463a345908ce6865c9c7894a9
```

> Note that the uuid `f8176c9463a345908ce6865c9c7894a9` will be different in your use case.

The job will perform the scoring and then save an updated CSV file with the prediction results:

![scoring-results](../../../../content/images/dashboard/runs/scoring-results.png)

We also logged the artifacts reference to the lineage tab:

![scoring-results-lineage](../../../../content/images/dashboard/runs/scoring-results-lineage.png)

## Running the job on schedule

You can put the job on schedule to perform scoring following eveytime the data is expected to change or following when the inputs CSV file is generated.

To run the job every Monday you can save and run the following polyaxonfile:

```yaml
version: 1.1
kind: operation
name: scoring-every-monday
schedule:
  kind: cron
  cron: "0 0 * * MON"
pathRef: ./polyaxonfile.yaml
```

You can also use an interval instead of a cron:

```yaml
version: 1.1
kind: operation
name: scoring-every-60-minute
schedule:
  kind: interval
  frequency: 3600
  dependsOnPast: true
pathRef: ./polyaxonfile.yaml
```

## Saving the custom job in the component hub

By adding more parameters to this job, users can save this component to their private hub and allow users to easily schedule the job using the CLI/UI.
