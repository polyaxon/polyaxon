---
title: "Projects"
sub_link: "artifacts-versioning/projects"
meta_title: "Polyaxon management UI - Projects"
meta_description: "Each project(Artifact) is the entity that manages runs promoted as artifacts versions created in Polyaxon or other system,
each artifact: Can have multiple versions, Can be published publicly or privately within your organization, Can define team and project level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

A `Project` is an abstraction that defines one or multiple artifacts created in Polyaxon or other system, it can:
 * have multiple versions.
 * be published publicly or privately within your organization.
 * define team and project level permissions.

## Project creation

You can version your artifacts in each project or create a project to manage artifacts from multiple projects using the CLI, API, or the UI.

![artifacts-create](../../../../content/images/dashboard/artifacts-versioning/artifacts-create.png)

Alternatively you can create a project using the CLI:

```bash
polyaxon project create --name OWNER_NAME/MODEL_NAME --description ... --tags tag1,tag2,...
```

And then configure the project features using the UI

![artifacts-features](../../../../content/images/dashboard/artifacts-versioning/artifacts-features.png)

## Project overview

You can view a project that manages the artifacts' versions using the project CLI or UI.

### CLI

```bash
polyaxon project get -p OWNER_NAME/MODEL_NAME
```

### UI

![artifacts-overview](../../../../content/images/dashboard/artifacts-versioning/artifacts-overview.png)

## Artifacts versions

### CLI

```bash
polyaxon artifacts ls -p OWNER_NAME/MODEL_NAME --query ... --sort ...
```

### UI

![artifacts-versions](../../../../content/images/dashboard/artifacts-versioning/artifacts-versions.png)

## Project admin

### CLI

Updating

```bash
polyaxon project update -p ...
```

Deleting

```bash
polyaxon project delete -p ...
```

### UI

You can manage a project using the UI, you can also manage who can contribute and have access to the artifacts versions,
as well as from which projects users are allowed to promote runs

![artifacts-admin](../../../../content/images/dashboard/artifacts-versioning/artifacts-admin.png)

