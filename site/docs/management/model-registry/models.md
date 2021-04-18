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

Model is an abstraction that defines a model created in Polyaxon or other system, it can:
 * have multiple versions.
 * be published publicly or privately within your organization.
 * define team and project level permissions.

## Model create

You can create your models using the CLI, API, or the UI.

### CLI

```bash
polyaxon registry create --name OWNER_NAME/MODEL_NAME --description ... --tags tag1,tag2,... 
```

### UI

![model-create](../../../../content/images/dashboard/registry/model-create.png)

## Model overview


### CLI

```bash
polyaxon registry get -m OWNER_NAME/MODEL_NAME
```

### UI

![model-overview](../../../../content/images/dashboard/registry/model-overview.png)

## Model versions

### CLI

```bash
polyaxon registry ls -m OWNER_NAME/MODEL_NAME --query ... --sort ...
```

### UI

![model-versions](../../../../content/images/dashboard/registry/model-versions.png)

## Model admin

### CLI

Updating

```bash
polyaxon registry update -m ...
```

Deleting

```bash
polyaxon registry delete -m ...
```

### UI

You can manage a model using the UI, you can also manage who can contribute and have access to the component and its versions, 
as well as from which projects users are allowed to promote experiments
 
![model-admin](../../../../content/images/dashboard/registry/model-admin.png)

