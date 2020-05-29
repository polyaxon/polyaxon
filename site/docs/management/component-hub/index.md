---
title: "Component Hub"
sub_link: "components-hub"
meta_title: "Polyaxon management UI - Agents"
meta_description: "Polyaxon Agent is the tool that allows to orchestrate runs on user's clusters."
tags:
    - concepts
    - polyaxon
    - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>
<blockquote class="info">This feature is still in Beta!</blockquote>


## Overview

Polyaxon Component Hub is a product for managing versioned and reusable components, each component:
 * Can have multiple versions.
 * Can be published publicly or privately within your organization.
 * Can define team level permissions.

![overview](../../../../content/images/dashboard/hub/overview.png)

Component is the entity in Polyaxon that defines a run time, it allows to package a containerize workload or a whole workflow, 
and makes it repeatable, portable, and sharable.

Polyaxon Component Hub gives you the extra utilities and features to manage access, security, and versioning.

## Understanding the component hub

Each component can have multiple versions, similar to docker images, to avoid breaking old experiments and workflows.

Each component can list all versions, their stage, their specification, and their usage.

![production-stage](../../../../content/images/dashboard/hub/production.png)

Polyaxon provides a special tag to signal the stage of your components versions. 
By default the Component Hub shows the latest version and its stage.

![testing-stage](../../../../content/images/dashboard/hub/testing.png)

## Creation

You can create a new component using the API or the dashboard, 
the component definition is the same [specification](/docs/core/specification/component/) that is used for running inline components. 
By using the `:tag`, you can add new version in to a component, Polyaxon uses the `owner/component-name` as a namespace for the component.

## Usage

As soon as a component is registered in your organization's hub, you can use it in your [operations](/docs/core/specification/operation/).

Using the cli:

```bash
polyaxon run --hub=org/mycomponent:v1.1 -P param1=value1 ...
```

Using the operation specification:

```yaml
version: 1.1
kind: operation
params:
  ...
hubRef: org/mycomponent:v1.1
```


Using the client:

```python
from polyaxon.client import RunClient

RunClient().create_from_hub(component="org/mycomponent:v1.1", name="execution5", params={...}, ...)
```
