---
title: "Component Hub"
sub_link: "component-hub"
is_index: true
meta_title: "Polyaxon management UI - Component Hub"
meta_description: "Polyaxon Component Hub is a product for managing versioned and reusable components,
each component: Can have multiple versions, Can be published publicly or privately within your organization, Can define team level permissions."
tags:
    - concepts
    - polyaxon
    - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Polyaxon Component Hub is a product for managing versioned and reusable components, each component:
 * Can have multiple versions.
 * Can be published publicly or privately within your organization.
 * Can define team level permissions.

![overview](../../../../content/images/dashboard/hub/overview.png)

`Component` is the entity in Polyaxon that defines a runtime, it allows to package a containerize workload or a whole workflow,
and makes it repeatable, portable, and sharable.

Polyaxon Component Hub gives you the extra utilities and features to manage access, security, and versioning.

## Understanding the component hub

Each component can have multiple versions, similar to docker images, to avoid breaking old experiments and workflows.

Each component can list all versions, their stage, their specification, and their usage.

Polyaxon provides a special tag to signal the stage of your components' versions.
By default, if a user runs a component without specifying the version, the Component Hub uses `latest` if it exists otherwise it will raise a 404 error.

## Managing and using components

You can create and manage components and versions using the API, CLI or the dashboard.

> Please check the component management guide. 

Each component version uses a definition which is the same [specification](/docs/core/specification/component/) that is used for running inline components.
By using `:tag`, you can add new versions to a component, Polyaxon uses the `owner/component-name` as a namespace for the component,
and will default to `component-name:version` when an owner is not specified. This is the public component managed by Polyaxon itself.

> Please check the component version management guide.

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
