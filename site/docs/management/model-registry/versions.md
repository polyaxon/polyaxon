---
title: "Model versions"
sub_link: "model-registry/versions"
meta_title: "Polyaxon management UI - Model Versions"
meta_description: "Model versions,
each model: Can have multiple versions, Can be published publicly or privately within your organization, Can define team and project level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

A model can have one or more versions, each version:

 * Can lock a specific run to track lineage.
 * Can be deployed as an internal app.
 * Can be deployed in production.

### CLI Reference

You can check the complete [models CLI reference here](/docs/core/cli/models/) or by using `polyaxon models --help`.

### Client Reference

Polyaxon's [ProjectClient](/docs/core/python-library/project-client/) library exposes all methods to:
 * [list_model_versions](/docs/core/python-library/project-client/#list_model_versions)
 * [get_model_version](/docs/core/python-library/project-client/#get_model_version)
 * [create_model_version](/docs/core/python-library/project-client/#create_model_version)
 * [patch_model_version](/docs/core/python-library/project-client/#patch_model_version)
 * [register_model_version](/docs/core/python-library/project-client/#register_model_version)
 * [copy_model_version](/docs/core/python-library/project-client/#copy_model_version)
 * [transfer_model_version](/docs/core/python-library/project-client/#transfer_model_version)
 * [delete_model_version](/docs/core/python-library/project-client/#delete_model_version)
 * [stage_model_version](/docs/core/python-library/project-client/#stage_model_version)
 * [pull_model_version](/docs/core/python-library/project-client/#pull_model_version)

Since `v1.18`, Polyaxon's [RunClient](/docs/core/python-library/run-client/) library exposes a method to automatically promote the run to a model version:
 * [promote_to_model_version](/docs/core/python-library/run-client/#promote_to_model_version)

## Model version creation

You can create your model versions using the CLI, API, or the UI.

### CLI

```bash
polyaxon models register -p OWNER_NAME/MODEL_NAME --version VERSION_NAME --description ... --tags tag1,tag2,... --artifacts model-name,env,asset-version
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

version = project_client.register_model_version(
    version="v1",
    description="description for this version...",
    tags=["prod"],
    content={"key": "val", "env": ["package1", "package2"]},
    run="f27c0580dcdf4ed7b2f36726c5257ade",
    artifacts=["model", "env"],
)
```

> **Note**: You can use `force=True` to override a previous version registered with the same name.

### UI

![version-create](../../../../content/images/dashboard/registry/version-create.png)

## Model version creation from a run

When a user create a run that tracks a model, users can promote a model version directly from a run:

![version-promote](../../../../content/images/dashboard/registry/version-promote.png)

Once a model version is registered, the run will be marked as promoted:

![version-promoted](../../../../content/images/dashboard/registry/version-promoted.png)

## Model version overview and definition

### CLI

```bash
polyaxon models get -ver VERSION_NAME
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

version = project_client.get_model_version(version="v1")
print(version)
```

### UI

![version-overview](../../../../content/images/dashboard/registry/version-overview.png)

## Model version stage changes

You can update the stage of the model version to reflect the production-readiness

### CLI

```bash
polyaxon models stage -ver VERSION_NAME -to staging --reason ModelTestGithubAction --message "Tests passed and the model was automatically moved to staging" ...
```

### Client

```python
from polyaxon.client import V1Stages
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

project_client.stage_model_version(
    version="v1",
    stage=V1Stages.STAGING,
    reason="AirflowPipelineStageUpdate",
    message="Tests passed and the model was automatically moved to staging",
)
```

## UI

![version-stage](../../../../content/images/dashboard/registry/version-stage.png)

## Model version admin

### CLI

You can override a model version with push:

```bash
polyaxon models register -ver ... --force
```

Or update specific info:

```bash
polyaxon models update -ver ...
```

and delete

```bash
polyaxon models delete -ver ...
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

# Update
project_client.patch_model_version(
    version="v1",
    data={"description": "new description", "tags": ["new-tag1", "new-tag2"]}
)

# Delete
project_client.delete_model_version(version="v1")
```

### UI

You can manage a model version using the UI

![version-admin](../../../../content/images/dashboard/registry/version-admin.png)

## Model version packaging and pulling

### CLI

```bash
polyaxon models pull -ver VERSION_NAME --help
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

project_client.pull_model_version(
    version="v1",
    path="/tmp/path"
)
```

## Model version promotion from a run tracking

### Client

```python
from polyaxon import tracking

tracking.init()

# Model lineage reference
model_ref = "model"

# Logging the model as pickle
with tempfile.TemporaryDirectory() as d:
    model_path = os.path.join(d, "model.pkl")
    with open(model_path, "wb") as out:
        pickle.dump(gbc, out)
    tracking.log_model(model_path, name=model_ref, framework="scikit-learn")

# Promoting the run to a model version
if some_condition:
    tracking.promote_to_model_version(
        version="rc2",
        description="model promoted directly from the run",
        tags=["tag1", "tag2"],
        content={"key": "value"},
        artifacts=[model_ref]
    )

# End
tracking.end()
```
