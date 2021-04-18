---
title: "Components"
sub_link: "component-hub/components"
meta_title: "Polyaxon management UI - Components"
meta_description: "Components is the entity that defines the runtime in Polyaxon,
each component: Can have multiple versions, Can be published publicly or privately within your organization, Can define team level permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Component is the abstraction that defines the runtime in Polyaxon, it can:
 * have multiple versions.
 * be published publicly or privately within your organization.
 * define team level permissions.
 * can have multiple versions, similar to docker images, to avoid breaking old experiments and workflows.


## Component create

You can create your components using the CLI, API, or the UI.

### CLI

```bash
polyaxon hub create --name OWNER_NAME/COMPONENT_NAME --description ... --tags tag1,tag2,... 
```

### UI

![component-create](../../../../content/images/dashboard/hub/component-create.png)

## Component overview


### CLI

```bash
polyaxon hub get -c OWNER_NAME/COMPONENT_NAME
```

### UI

![component-overview](../../../../content/images/dashboard/hub/component-overview.png)

## Component versions

### CLI

```bash
polyaxon hub ls -c OWNER_NAME/COMPONENT_NAME --query ... --sort ...
```

### UI

![component-versions](../../../../content/images/dashboard/hub/component-versions.png)

## Component admin

### CLI

Updating

```bash
polyaxon hub update -c ...
```

Deleting

```bash
polyaxon hub delete -c ...
```

### UI

You can manage a component using the UI, you can also manage who can contribute and have access to the component and its versions
 
![component-admin](../../../../content/images/dashboard/hub/component-admin.png)

