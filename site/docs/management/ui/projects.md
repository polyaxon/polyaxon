---
title: "Projects"
sub_link: "ui/projects"
meta_title: "Projects in Polyaxon - Management UI"
meta_description: "A Project in Polyaxon is very similar to a project in GitHub, it aims at organizing your efforts to solve a specific problem."
tags:
    - concepts
    - polyaxon
    - management
sidebar: "management"
---

A `Project` in Polyaxon is very similar to a project in GitHub,
it aims at organizing your efforts to solve a specific problem.

## Create new project

To create a project, you can either use the Polyaxon Dashboard or the Polyaxon CLI.

The projects consist of a required argument `--name`, an optional argument `--description`,
and a flag `--private` with a default value set to `False`.

The projects could be `public` (default behaviour) or `private`.


```bash
$ polyaxon project create --name=mnist --description='Classification of handwritten images.'
```

> For more details about this command please run `polyaxon project create --help`, 
or check the [command reference](/references/polyaxon-cli/project/#create)

The project is created by default `public`, to make it private please add `--private`

Creating project with the UI

![project-create](../../../../content/images/dashboard/projects/create.png)

## Project overview

Every project can manage jobs, services, dags, matrix executions.

![project-overview](../../../../content/images/dashboard/projects/overview.png)

## Project settings

The project settings page provides several tabs to manage accessible members, teams, run profiles, connections, ...

![project-settings-select](../../../../content/images/dashboard/projects/settings-select.png)

The general settings page

![project-settings](../../../../content/images/dashboard/projects/settings.png)


## Default settings

By default when a project is created, it will be accessible to all the organization's members following their roles on the organizations level.
In order to restrict teams, connections, profiles, ..., you need to manually define the resources and teams that can access using the settings tabs. 

Example restricting teams access

![project-teams-settings](../../../../content/images/dashboard/projects/teams-settings.png)
