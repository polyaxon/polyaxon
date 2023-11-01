---
title: "Artifact versions"
sub_link: "artifacts-versioning/versions"
meta_title: "Polyaxon management UI - Artifact Versions"
meta_description: "Artifact versions,
each artifact: Can have multiple versions, Can be published publicly or privately within your organization, can define team and project level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

A project can have one or more artifact versions, each version:

 * Can lock a specific run to track lineage.
 * Can be deployed as an internal app.
 * Can be deployed in production.


### CLI Reference

You can check the complete [artifacts CLI reference here](/docs/core/cli/artifacts/) or by using `polyaxon artifacts --help`.

### Client Reference

Polyaxon's [ProjectClient](/docs/core/python-library/project-client/) library exposes all methods to:
 * [list_artifact_versions](/docs/core/python-library/project-client/#list_artifact_versions)
 * [get_artifact_version](/docs/core/python-library/project-client/#get_artifact_version)
 * [create_artifact_version](/docs/core/python-library/project-client/#create_artifact_version)
 * [patch_artifact_version](/docs/core/python-library/project-client/#patch_artifact_version)
 * [register_artifact_version](/docs/core/python-library/project-client/#register_artifact_version)
 * [copy_artifact_version](/docs/core/python-library/project-client/#copy_artifact_version)
 * [transfer_artifact_version](/docs/core/python-library/project-client/#transfer_artifact_version)
 * [delete_artifact_version](/docs/core/python-library/project-client/#delete_artifact_version)
 * [stage_artifact_version](/docs/core/python-library/project-client/#stage_artifact_version)
 * [pull_artifact_version](/docs/core/python-library/project-client/#pull_artifact_version)

Since `v1.18`, Polyaxon's [RunClient](/docs/core/python-library/run-client/) library exposes a method to automatically promote the run to an artifact version:
 * [promote_to_artifact_version](/docs/core/python-library/run-client/#promote_to_artifact_version)

## Artifact version creation

You can create your artifact versions using the CLI, API, or the UI.

### CLI

```bash
polyaxon artifacts register -p OWNER_NAME/PROJECT_NAME --version VERSION_NAME --description ... --tags tag1,tag2,... --artifacts artifact-name,env,summary
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/data-generation")

version = project_client.register_artifact_version(
    version="v1",
    description="description for this version...",
    tags=["prod", "images"],
    content={"key": "val", "env": ["package1", "package2"]},
    run="f27c0580dcdf4ed7b2f36726c5257ade",
    artifacts=["dataset", "summary"],
)
```

> **Note**: You can use `force=True` to override a previous version registered with the same name.


### UI

![version-create](../../../../content/images/dashboard/artifacts-versioning/version-create.png)

## Artifact version creation from a run

When a user create a run that tracks an artifact, users can promote that artifact version directly from a run:

![version-promote](../../../../content/images/dashboard/artifacts-versioning/version-promote.png)

Once an artifact version is registered, the run will be marked as promoted:

![version-promoted](../../../../content/images/dashboard/artifacts-versioning/version-promoted.png)

## Artifact version overview and definition

### CLI

```bash
polyaxon artifacts get [-p] -ver VERSION_NAME
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

version = project_client.get_artifact_version(version="v1")
print(version)
```

### UI

![version-overview](../../../../content/images/dashboard/artifacts-versioning/version-overview.png)

## Artifact version stage changes

You can update the stage of the artifact version to reflect the production-readiness

### CLI

```bash
polyaxon artifacts stage -ver VERSION_NAME -to staging --reason CISystem --message "Drift tests passed, move to staging" ...
```

### Client

```python
from polyaxon.client import V1Stages
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

project_client.stage_artifact_version(
    version="v1",
    stage=V1Stages.STAGING,
    reason="AirflowPipelineStageUpdate",
    message="Tests passed and the artifact was automatically moved to staging",
)
```

## UI

![version-stage](../../../../content/images/dashboard/artifacts-versioning/version-stage.png)


## Artifact version admin

### CLI

You can override an artifact version with push:

```bash
polyaxon artifacts register -ver ... --force
```

Or update specific info:

```bash
polyaxon artifacts update -ver ...
```

and delete

```bash
polyaxon artifacts delete -ver ...
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

# Update
project_client.patch_artifact_version(
    version="v1",
    data={"description": "new description", "tags": ["new-tag1", "new-tag2"]}
)

# Delete
project_client.delete_artifact_version(version="v1")
```


### UI

You can manage an artifact version using the UI

![version-admin](../../../../content/images/dashboard/artifacts-versioning/version-admin.png)

## Artifact version packaging and pulling

### CLI

```bash
polyaxon artifacts pull -ver VERSION_NAME --help
```

### Client

```python
from polyaxon.client import ProjectClient

project_client = ProjectClient(project="ORGANIZATION/bot-detection")

project_client.pull_artifact_version(
    version="v1",
    path="/tmp/path"
)
```

## Artifact version promotion from a run tracking

### Client

```python
from polyaxon import tracking

tracking.init()

# Artifact lineage reference
artifact_ref = "dataset-view"

# Logging a reference
tracking.log_artifact_ref("path/to/artifact", name=artifact_ref)

# Promoting the run to an artifact version
if some_condition:
    tracking.promote_to_artifact_version(
        version="rc2",
        description="artifact promoted directly from the run",
        tags=["tag1", "tag2"],
        content={"key": "value"},
        artifacts=[artifact_ref]
    )

# End
tracking.end()
```
