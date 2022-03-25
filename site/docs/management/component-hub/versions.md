---
title: "Component versions"
sub_link: "component-hub/versions"
meta_title: "Polyaxon management UI - Component Versions"
meta_description: "Component versions ,
each component: Can have multiple versions, Can be published publicly or privately within your organization, Can define team level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

A component can have one or more versions, each version:
 * Conveys useful information about a specific component version/variant.
 * Reflects changes in the logic of your component where previous versions are still used or referenced by runs.
 * Can have multiple versions, similar to docker images, to avoid breaking old experiments and workflows.

## Component version creation

You can create your component versions using the CLI, API, or the UI.

### CLI

```bash
polyaxon components register --version OWNER_NAME/COMPONENT_NAME[:tag] --description ... --tags tag1,tag2,... -f path/to/polyaxonfile.yaml 
```

### UI

![version-create](../../../../content/images/dashboard/hub/version-create.png)

## Component version creation from a run

When a user create a run, Polyaxon by default snapshot the component used and tag the run with the component version. Users can optionally promote a component version directly from a run:

![version-promote](../../../../content/images/dashboard/hub/version-promote.png)

Once a component is registered, any future run will be linked to it. Users can filter all runs using a specific component version:

![version-promoted](../../../../content/images/dashboard/hub/version-promoted.png)

## Component version overview and definition

### CLI

```bash
polyaxon components get -ver VERSION_NAME -p OWNER/PROJECT_NAME
```

### UI

![version-overview](../../../../content/images/dashboard/hub/version-overview.png)



![version-definition](../../../../content/images/dashboard/hub/version-definition.png)

## Component version admin

### CLI

You can override a component version with push:

```bash
polyaxon components register -f ./path/to/polyaxonfile.yaml -ver VERSION_NAME ... --push
```

Or update specific info:

```bash
polyaxon components update -ver ...
```

and delete  

```bash
polyaxon components delete -ver ...
```

### UI

You can manage a component version using the UI

![version-admin](../../../../content/images/dashboard/hub/version-admin.png)

And you can reflect the production-readiness using the stage setting

![version-stage](../../../../content/images/dashboard/hub/version-stage.png)
