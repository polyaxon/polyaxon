---
title: "Projects"
sub_link: "projects/general"
meta_title: "Projects in Polyaxon - Management UI"
meta_description: "A Project in Polyaxon is very similar to a project in GitHub, it aims at organizing your efforts to solve a specific problem."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

## Create a new project

You can create a project to store component versions using the CLI, API, or the UI.

### CLI

A project consists of a required argument `--name`, an optional argument `--description`,
and a flag `--private` with a default value set to `True`.

Projects could be `private` (default behavior) or `public`.


```bash
polyaxon project create --name=mnist --description='Classification of handwritten images.'
```

> For more details about this command please run `polyaxon project create --help`, or check the [command reference](/docs/core/cli/project/#create)

All projects are created by default `private`, you can change this behavior by adding `--public`

### UI

To create projects with the UI

![project-create](../../../../content/images/dashboard/projects/create.png)

### Project features

Project features allows to set the purpose of a project. Most project should take advantage of all features, but sometimes the purpose of a project is to store components, models, or artifacts only.

## Project overview

Every project can manage jobs, services, dags, and matrix executions. It also allows to promote runs to model or artifact versions, and store runnable components.

### CLI

```bash
polyaxon project get -c OWNER_NAME/COMPONENT_NAME
```

### UI

![project-overview](../../../../content/images/dashboard/projects/overview.png)
