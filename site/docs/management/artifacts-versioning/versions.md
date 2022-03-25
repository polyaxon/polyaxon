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

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

A project can have one or more artifact versions, each version:

 * Can lock a specific run to track lineage.
 * Can be deployed as an internal app.
 * Can be deployed in production.

## Artifact version creation

You can create your artifact versions using the CLI, API, or the UI.

### CLI

```bash
polyaxon artifacts register -p OWNER_NAME/MODEL_NAME --version VERSION_NAME --description ... --tags tag1,tag2,... --artifacts artifact-name,env,summary 
```

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

### UI

![version-overview](../../../../content/images/dashboard/artifacts-versioning/version-overview.png)

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

### UI

You can manage an artifact version using the UI

![version-admin](../../../../content/images/dashboard/artifacts-versioning/version-admin.png)

And you can reflect the production-readiness using the stage setting

![version-stage](../../../../content/images/dashboard/artifacts-versioning/version-stage.png)
