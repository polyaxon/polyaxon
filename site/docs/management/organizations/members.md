---
title: "Members"
sub_link: "organizations/members"
meta_title: "Polyaxon management tools and UI - Members"
meta_description: "You can invite members to your organization members and assign roles with specific permissions."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Membership in Polyaxon is handled at the organizational level.
The system is designed so each end user is assigned to a single Polyaxon account, which can then join one or more organizations.

Each end user should have their own account, where they can manage their personal preferences and security settings.

You can invite members to your organization members and assign roles with specific permissions.

## Organization members

After creating an organization, you can invite or remove members using the organization's settings.

![organization-invite](../../../../content/images/dashboard/orgs/invite.png)

You can also update their roles.

![organization-roles](../../../../content/images/dashboard/orgs/roles.png)


## Organization permissions

| Action                                                       | Viewer | Member | Admin | Manager | Owner | Billing |
| ------------------------------------------------------------ | ------ | ------ | ----- | ------- | ----- | ------- |
| Can see/edit billing information and subscription details    |        |        |       |         | X     | X       |
| Can remove an organization                                   |        |        |       |         | X     |         |
| Can change an organization's visibility                      |        |        |       |         | X     |         |
| Can change an organization's settings                        |        |        |       | X       | X     |         |
| Can add/remove/change a team                                 |        |        |       | X       | X     |         |
| Can add/remove/change a member                               |        |        |       | X       | X     |         |
| Can add/remove/change an agent                               |        |        |       | X       | X     |         |
| Can add/remove/change an preset                              |        |        |       | X       | X     |         |
| Can edit global integrations                                 |        |        |       | X       | X     |         |
| Can view an organization's level analytics                   |        |        | X     | X       | X     |         |
| Can view an organization's level activity logs               |        |        | X     | X       | X     |         |
| Can add/remove/change a project                              |        |        | X     | X       | X     |         |
| Can change a project's settings                              |        |        | X     | X       | X     |         |
| Can change a project's permissions                           |        |        | X     | X       | X     |         |
| Can add/remove/change a component hub                        |        |        | X     | X       | X     |         |
| Can change a component hub's settings                        |        |        | X     | X       | X     |         |
| Can change a component hub's permissions                     |        |        | X     | X       | X     |         |
| Can add/remove/change a model registry                       |        |        | X     | X       | X     |         |
| Can change a model registry's settings                       |        |        | X     | X       | X     |         |
| Can change a model registry's permissions                    |        |        | X     | X       | X     |         |
| Can create/update runs                                       |        | X      | X     | X       | X     |         |
| Can delete runs                                              |        |        | X     | X       | X     |         |
| Can create/update searches                                   |        | X      | X     | X       | X     |         |
| Can delete searches                                          |        |        | X     | X       | X     |         |
| Can promote searches to the organization level               |        |        | X     | X       | X     |         |
| Can create/update dashboards                                 |        | X      | X     | X       | X     |         |
| Can delete dashboards                                        |        |        | X     | X       | X     |         |
| Can promote dashboards to the organization level             |        |        | X     | X       | X     |         |
| Can create/update component versions                         |        | X      | X     | X       | X     |         |
| Can delete component versions                                |        |        | X     | X       | X     |         |
| Can create/update model versions                             |        | X      | X     | X       | X     |         |
| Can delete model versions                                    |        |        | X     | X       | X     |         |
| Can view projects, runs and related metadata and artifacts   | X      | X      | X     | X       | X     |         |
| Can view component hub and versions                          | X      | X      | X     | X       | X     |         |
| Can view model registry and versions                         | X      | X      | X     | X       | X     |         |


## Organization roles

Member roles dictate access within an organization.

### Owner

Unrestricted access to the organization, its data, and settings.

 * Gains full permission across the organization.
 * Can add, modify, and delete projects, components, models, and members.
 * Can manage members.
 * Can make billing and plan changes.
 * Can delete an organization.

### Billing

> **Note**: Available on EE or to organizations with **Pro features**

 * Has access to the billing information only.
 * Can manage subscription and billing details.

### Manager

> **Note**: Available on EE or to organizations with **Pro features**

 * Has similar access as an **Owner**.
 * Does not have access to `billing`.
 * Cannot delete the organization.
 * Cannot change the organization's visibility (public/private).

### Admin

 * Does not have access to the organization settings. 
 * Has admin privileges on any teams of which they're a member.
 * Can admin projects and set restrictions on connections, presets, members access, agents, queues.
 * Can create new teams, projects, model registry and component hub entries.
 * Can remove teams, projects, model registry and component hub entries which they already hold membership on.
 * Can promote searches and dashboards to organization level.
 * Can promote experiments to model registry.

### Member
 
 * Can view project, models, components.
 * Can view experiments, jobs, builds, services, dashboards, pipelines.
 * Can act on experiments, jobs, builds, services, dashboards, pipelines.
 * Can view most other data within the organization.

### Viewer

 * Can view experiments, jobs, builds, services, dashboards, pipelines.
 * Can view most other data within the organization.

### Outsider

> **Note**: Available on EE or to organizations with **Pro features**

 * Is a person who isn't explicitly a member of your organization.
 * Can read, write, or have admin permissions to one or more projects in your organization if invited and provided with such permissions.


## Managing users and permissions

Users with the `owner` role can promote, demote, and delete all users up to the `owner` level.

Users with the `manager` role can manage all users except users with the `owner` role.

Users with the `admin` role can only manage configurations and restrictions on the project, model registry, and component hub level.

## Team level roles

Users with `outsider`, `viewer`, `member`, and `admin` can be invited to teams and they can be promoted up-to the `admin` level role, e.g. `outisder` -> `member`, `member` -> `admin`.

Each project, component hub, model registry can restrict access by selecting users and teams. 
If teams are selected, users will act based on the highest role they have in the teams they belong to and have access to that entity.

Please check [teams section](/docs/management/organizations/teams/) for more details.

## Re-assigning seats

By removing a user from the members table, you can re-invite or add a different user based on a new email.
Only users with the `owner` and `manager` roles can add/remove users, in fact, 
only these two roles have access to the organization level settings.
