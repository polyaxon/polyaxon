---
title: "Models"
sub_link: "model-registry/models"
meta_title: "Polyaxon management UI - Models"
meta_description: "Models is the entity that defines the a version of a model created in Polyaxon or other system,
each model: Can have multiple versions, Can be published publicly or privately within your organization, Can define team and project level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

A `Model` is an abstraction that defines a model created in Polyaxon or other system, it can:
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
polyaxon project get -m OWNER_NAME/MODEL_NAME
```

### UI

![model-overview](../../../../content/images/dashboard/registry/model-overview.png)

## Model versions

### CLI

```bash
polyaxon models ls -m OWNER_NAME/MODEL_NAME --query ... --sort ...
```

### UI

![model-versions](../../../../content/images/dashboard/registry/model-versions.png)

## Model admin

### CLI

Updating

```bash
polyaxon project update -m ...
```

Deleting

```bash
polyaxon project delete -m ...
```

### UI

You can manage a model using the UI, you can also manage who can contribute and have access to the component and its versions, 
as well as from which projects users are allowed to promote experiments
 
![model-admin](../../../../content/images/dashboard/registry/model-admin.png)

