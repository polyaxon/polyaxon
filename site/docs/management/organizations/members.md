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

You can invite members to your organization members and assign roles with specific permissions.

## Organization members

After creating an organization, you can invite or remove members using the organization's settings.

![organization-invite](../../../../content/images/dashboard/orgs/invite.png)

You can also update their roles.

![organization-roles](../../../../content/images/dashboard/orgs/roles.png)


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


## Re-assigning seats

By removing a user from the members table, you can re-invite or add a different user based on a new email.
Only users with the `owner` and `manager` roles can add/remove users, in fact, 
only these two roles have access to the organization level settings.

## Managing users and permissions

Users with the `owner` can promote, demote, and delete all users up to the `owner` level.

Users with the `manager` role can manage all users except users with the `owner` role.

Users with the `admin` role can only manage configurations and restrictions on the project, model registry, and component hub level.
