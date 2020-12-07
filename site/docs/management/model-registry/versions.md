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

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

A model can have one or more versions, each version:

 * Can lock a specific run to track lineage.
 * Can be deployed as an internal app.
 * Can be deployed in production.

## Model version create

You can create your model versions using the CLI, API, or the UI.

### CLI

```bash
polyaxon registry push --name OWNER_NAME/MODEL_NAME[:tag] --description ... --tags tag1,tag2,... -f path/to/polyaxonfile.yaml 
```

### UI

![version-create](../../../../content/images/dashboard/registry/version-create.png)

## Model version overview and definition

### CLI

```bash
polyaxon registry get -ver OWNER_NAME/MODEL_NAME[:tag]
```

### UI

![version-overview](../../../../content/images/dashboard/registry/version-overview.png)

## Model version admin

### CLI

You can override a model version with push:

```bash
polyaxon registry push --name ...
```

Or update specific info:

```bash
polyaxon registry update -ver ...
```

and delete  

```bash
polyaxon registry delete -ver ...
```

### UI

You can manage a model version using the UI

![version-admin](../../../../content/images/dashboard/registry/version-admin.png)

And you can reflect the production-readiness using the stage setting

![version-stage](../../../../content/images/dashboard/registry/version-stage.png)
