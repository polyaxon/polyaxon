---
title: "Projects (Models)"
sub_link: "model-registry/projects"
meta_title: "Polyaxon management UI - Models"
meta_description: "Each project(Model) is the entity that manages runs promoted as model versions created in Polyaxon or other system,
each model: Can have multiple versions, Can be published publicly or privately within your organization, Can define team and project level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

A `Model` is a project that manages several versions of a model asset created in Polyaxon or other system, it can:
 * have multiple versions.
 * be published publicly or privately within your organization.
 * define team and project level permissions.

## Model project creation

You can version your models in each project or create a project to manage models from multiple projects using the CLI, API, or the UI.

![model-create](../../../../content/images/dashboard/registry/model-create.png)

Alternatively you can create a project using the CLI:

```bash
polyaxon project create --name OWNER_NAME/MODEL_NAME --description ... --tags tag1,tag2,...
```

And then configure the project features using the UI

![model-features](../../../../content/images/dashboard/registry/model-features.png)

## Model overview

You can view a model overview using the project CLI or UI.

### CLI

```bash
polyaxon project get -p OWNER_NAME/MODEL_NAME
```

### UI

![model-overview](../../../../content/images/dashboard/registry/model-overview.png)

## Model versions

### CLI

```bash
polyaxon models ls -p OWNER_NAME/MODEL_NAME --query ... --sort ...
```

### UI

![model-versions](../../../../content/images/dashboard/registry/model-versions.png)

## Model admin

### CLI

Updating

```bash
polyaxon project update [-p] [-ver]...
```

Deleting

```bash
polyaxon project delete [-p] [-ver]...
```

### UI

You can manage a project(model) using the UI, you can also manage who can contribute and have access to the project and the model versions,
as well as from which projects users are allowed to promote runs

![model-admin](../../../../content/images/dashboard/registry/model-admin.png)

