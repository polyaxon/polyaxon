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

## Overview

A component can have one or more versions, each version:
 * Conveys useful information about a specific component version/variant.
 * Reflects changes in the logic of your component where previous versions are still used or referenced by runs.
 * Can have multiple versions, similar to docker images, to avoid breaking old experiments and workflows.

### CLI Reference

You can check the complete [components CLI reference here](/docs/core/cli/components/) or by using `polyaxon components --help`.

### Client Reference

Polyaxon's [ProjectClient](/docs/core/python-library/project-client/) library exposes all methods to:
 * [list_component_versions](/docs/core/python-library/project-client/#list_component_versions)
 * [get_component_version](/docs/core/python-library/project-client/#get_component_version)
 * [create_component_version](/docs/core/python-library/project-client/#create_component_version)
 * [patch_component_version](/docs/core/python-library/project-client/#patch_component_version)
 * [register_component_version](/docs/core/python-library/project-client/#register_component_version)
 * [copy_component_version](/docs/core/python-library/project-client/#copy_component_version)
 * [transfer_component_version](/docs/core/python-library/project-client/#transfer_component_version)
 * [delete_component_version](/docs/core/python-library/project-client/#delete_component_version)
 * [stage_component_version](/docs/core/python-library/project-client/#stage_component_version)
 * [pull_component_version](/docs/core/python-library/project-client/#pull_component_version)

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

## Component version stage changes

You can update the stage of the component version to reflect the production-readiness

### CLI

```bash
polyaxon components stage -ver VERSION_NAME -to production ...
```

## UI

![version-stage](../../../../content/images/dashboard/hub/version-stage.png)

## Component version admin

### CLI

You can override a component version with the `--force` flag:

```bash
polyaxon components register -f ./path/to/polyaxonfile.yaml -ver VERSION_NAME ... --force
```

Or update specific info:

```bash
polyaxon components update -ver ...
```

Or delete the version:

```bash
polyaxon components delete -ver ...
```

### UI

You can manage a component version using the UI

![version-admin](../../../../content/images/dashboard/hub/version-admin.png)
