---
title: "Project settings"
sub_link: "projects/settings"
meta_title: "Project settings - Management UI"
meta_description: "Every Project has settings to archive, restrict access, set defaults ..."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Project settings

The project settings page provides several tabs to manage accessible members, teams, presets, connections, ...

![project-settings-select](../../../../content/images/dashboard/projects/settings-select.png)

The general settings page lets you change the project's details

![project-settings](../../../../content/images/dashboard/projects/settings.png)


Users can also use the CLI to perform admin operations:

Updates

```bash
polyaxon project update -c ...
```

Deletion

```bash
polyaxon project delete -c ...
```

## Default Queue and Preset

When a project is created, it will use the default organization queue and the default organization preset if defined.
You can define defaults values that should be used by each project:

![project-teams-settings](../../../../content/images/dashboard/projects/default-settings.png)


## Access settings

When a project is created, it will be accessible to all organization's members following their roles on the organization level.
In order to restrict teams, connections, profiles, ..., you need to manually define the teams that can access the project and the resources that can be accessed, using the settings tabs.

Example restricting teams access

![project-teams-settings](../../../../content/images/dashboard/projects/teams-settings.png)


Example restricting agents

![project-agents-settings](../../../../content/images/dashboard/projects/agents-settings.png)


Example restricting queues

![project-agents-settings](../../../../content/images/dashboard/projects/queues-settings.png)
