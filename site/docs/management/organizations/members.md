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
You can invite members to your organization and assign them roles with specific permissions.

## Organization membership

Polyaxon comes with the following membership roles:
 * [Owner](/docs/management/organizations/members/#owner)
 * [Manager (Organization Level Admin)](/docs/management/organizations/members/#manager)
 * [Admin (Project Level Admin)](/docs/management/organizations/members/#admin)
 * [Member](/docs/management/organizations/members/#member)
 * [Viewer](/docs/management/organizations/members/#viewer)

After creating an organization, you can invite or remove members using the organization's settings:

![organization-invite](../../../../content/images/dashboard/orgs/invite.png)

You can also update their roles:

![organization-roles](../../../../content/images/dashboard/orgs/roles.png)


## Organization permissions

| Action                                                       | Viewer | Member | Admin | Manager | Owner  | Billing |
| ------------------------------------------------------------ | ------ | ------ | ----- | ------- | ------ | ------- |
| Can see/edit billing information and subscription details    |        |        |       |         | ✅     | ✅      |
| Can remove an organization                                   |        |        |       |         | ✅     |         |
| Can change an organization's visibility                      |        |        |       |         | ✅     |         |
| Can change an organization's settings                        |        |        |       | ✅      | ✅     |         |
| Can add/remove/change a team                                 |        |        |       | ✅      | ✅     |         |
| Can add/remove/change a member                               |        |        |       | ✅      | ✅     |         |
| Can add/remove/change an agent                               |        |        |       | ✅      | ✅     |         |
| Can add/remove/change a preset                               |        |        |       | ✅      | ✅     |         |
| Can edit global integrations                                 |        |        |       | ✅      | ✅     |         |
| Can manage an organization's cross-project runs              |        |        | ✅    | ✅      | ✅     |         |
| Can view an organization's level analytics                   |        |        | ✅    | ✅      | ✅     |         |
| Can view an organization's level activity logs               |        |        | ✅    | ✅      | ✅     |         |
| Can add/remove/change a project                              |        |        | ✅    | ✅      | ✅     |         |
| Can change a project's settings                              |        |        | ✅    | ✅      | ✅     |         |
| Can change a project's permissions                           |        |        | ✅    | ✅      | ✅     |         |
| Can add/remove/change a component hub                        |        |        | ✅    | ✅      | ✅     |         |
| Can change a component hub's settings                        |        |        | ✅    | ✅      | ✅     |         |
| Can change a component hub's permissions                     |        |        | ✅    | ✅      | ✅     |         |
| Can add/remove/change a model registry                       |        |        | ✅    | ✅      | ✅     |         |
| Can change a model registry's settings                       |        |        | ✅    | ✅      | ✅     |         |
| Can change a model registry's permissions                    |        |        | ✅    | ✅      | ✅     |         |
| Can create/update runs                                       |        | ✅     | ✅    | ✅      | ✅     |         |
| Can delete runs                                              |        |        | ✅    | ✅      | ✅     |         |
| Can create/update searches                                   |        | ✅     | ✅    | ✅      | ✅     |         |
| Can delete searches                                          |        |        | ✅    | ✅      | ✅     |         |
| Can promote searches to the organization level               |        |        | ✅    | ✅      | ✅     |         |
| Can create/update dashboards                                 |        | ✅     | ✅    | ✅      | ✅     |         |
| Can delete dashboards                                        |        |        | ✅    | ✅      | ✅     |         |
| Can promote dashboards to the organization level             |        |        | ✅    | ✅      | ✅     |         |
| Can create/update component versions                         |        | ✅     | ✅    | ✅      | ✅     |         |
| Can delete component versions                                |        |        | ✅    | ✅      | ✅     |         |
| Can create/update model versions                             |        | ✅     | ✅    | ✅      | ✅     |         |
| Can delete model versions                                    |        |        | ✅    | ✅      | ✅     |         |
| Can view projects                                            | ✅     | ✅     | ✅    | ✅      | ✅     |         |
| Can view a project's level analytics                         | ✅     | ✅     | ✅    | ✅      | ✅     |         |
| Can view a project's level activity logs                     | ✅     | ✅     | ✅    | ✅      | ✅     |         |
| Can view runs and related metadata and artifacts             | ✅     | ✅     | ✅    | ✅      | ✅     |         |
| Can view component hub and versions                          | ✅     | ✅     | ✅    | ✅      | ✅     |         |
| Can view model registry and versions                         | ✅     | ✅     | ✅    | ✅      | ✅     |         |


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

> **Note**: Available on EE and Business plans 

 * Has access to the billing information only.
 * Can manage subscription and billing details.

### Manager (Organization admin)

> **Note**: Available on EE and Business plans

 * Has similar access as an **Owner**.
 * Does not have access to `billing`.
 * Cannot delete the organization.
 * Cannot change the organization's visibility (public/private).

### Admin (Project admin)

 * Does not have access to the organization settings. 
 * Has admin privileges on any teams of which they're a member.
 * Can admin projects and set restrictions on connections, presets, members access, agents, queues.
 * Can create new projects, model registry and component hub entries.
 * Can remove projects, model registry and component hub entries which they already hold membership on.
 * Can manage and update settings of projects, model registry and component hub entries which they already hold membership on.
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

> **Note**: Available on EE and Business plans

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

## Team spaces

> **Coming soon**

Organization owners and managers can create space/group and delegate management to users following their team's roles instead of their organization roles.

When promoting a viewer or a member to the admin role on a specific team, the user cannot create projects/models/components and still requires an organization's level admin to perform those operations.

A team space (or a group) provides a view of the organization where users can act based on their roles in a specific team, 
which should allow the users in that team to be fully autonomous within that specific space and can act following the role they have on that team.

The team space/group allows as well to reduce the amount of work required from an organization's admin to bootstrap new projects for their users, i.e. within a team space any new project will inherit all restrictions and default configurations such as presets, runtimes, connections, ... 

Please check [teams section](/docs/management/organizations/teams/) for more details.

## Re-assigning seats

By removing a user from the members table, you can re-invite or add a different user based on a new email.
Only users with the `owner` and `manager` roles can add/remove users, in fact, 
only these two roles have access to the organization level settings.
