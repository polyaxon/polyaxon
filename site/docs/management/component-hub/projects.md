---
title: "Projects (Components)"
sub_link: "component-hub/projects"
meta_title: "Polyaxon management UI - Components"
meta_description: "Components is the entity that defines the runtime in Polyaxon,
each component: Can have multiple versions, Can be published publicly or privately within your organization, Can define team level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Overview

A `Component` is the abstraction that defines the runtime in Polyaxon, it can:
 * have multiple versions.
 * be published publicly or privately within your organization.
 * define team level permissions.
 * can have multiple versions, similar to docker images, to avoid breaking old experiments and workflows.

## Component project creation

In order to store multiple related versions of a Polyaxonfile, users can create a project that enables only the `component` feature:

![component-create](../../../../content/images/dashboard/hub/component-create.png)

Alternatively you can create a project using the CLI:

```bash
polyaxon project create --name OWNER_NAME/COMPONENT_NAME --description ... --tags tag1,tag2,...
```

And then configure the project features using the UI

![component-features](../../../../content/images/dashboard/hub/component-features.png)

## Component overview

You can view a component overview using the project CLI or UI.

### CLI

```bash
polyaxon project get -p OWNER_NAME/COMPONENT_NAME
```

### UI

![component-overview](../../../../content/images/dashboard/hub/component-overview.png)

## Component project versions

### CLI

```bash
polyaxon components ls -p OWNER_NAME/PROJECT_NAME --query ... --sort ...
```

### UI

![component-versions](../../../../content/images/dashboard/hub/component-versions.png)

## Component project admin

### CLI

Updating

```bash
polyaxon project update -p ...
```

Deleting


```bash
polyaxon project delete -p ...
```

You can manage a component using the UI, you can also manage who can contribute and have access to the component and its versions

![component-admin](../../../../content/images/dashboard/hub/component-admin.png)
