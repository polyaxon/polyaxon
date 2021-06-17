---
title: "Presets"
sub_link: "organizations/presets"
meta_title: "Polyaxon management tools and UI - Presets"
meta_description: "Scheduling presets is a feature for injecting certain information into operations at compilation time to preset configuration for node scheduling,
queue routing, resources requirements and definition, connections, and access level control."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

Scheduling presets is a feature for injecting certain information into operations at compilation time to preset configuration for node scheduling,
queue routing, resources requirements and definition, connections, and access level control.

Polyaxon allows to save these presets as Polyaxonfiles, and to use them interactively using Polyaxon CLI. 
Sometimes, some of these presets are generic and can be used in all projects, or you want to configure default 
manifests to be applied to all operations started by a user or in a specific project. 
You can save presets in your organization, and allow users to use them in their Polyaxonfiles.

## Create scheduling presets

If you have admin access you can create new scheduling preset.

![presets-create](../../../../content/images/dashboard/presets/create.png)


## Manage scheduling presets

You can list, review, and manage all scheduling presets.

![presets-manage](../../../../content/images/dashboard/presets/manage.png)

## Presets settings

You can update or delete a scheduling preset.

![presets-settings](../../../../content/images/dashboard/presets/settings.png)

## Presets viewer and usage

Users without admin or owner rights can view the table of available presets in your organization and how they can use them.

![presets-usage](../../../../content/images/dashboard/presets/usage.png)


## Global or per project default preset

Managers and Admins of Polyaxon organizations and projects can set a default preset that gets applied to all runs under the organization or the project.

Setting the organization's default preset:

![default-org-preset](../../../../content/images/dashboard/presets/default-org-preset.png)

Setting a project's default preset:

![default-project-preset](../../../../content/images/dashboard/presets/default-project-preset.png) 
