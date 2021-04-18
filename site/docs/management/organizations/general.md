---
title: "Organizations"
sub_link: "organizations/general"
meta_title: "Polyaxon management tools and UI - Organizations"
meta_description: "Organizations are an entity where businesses can collaborate across many projects at once."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

Organizations are an entity where businesses can collaborate across many projects at once.
Owners and administrators can manage member access to the organization's data, projects, models, and components with sophisticated security and administrative features.
Organizations can also have analytics, activities, and insights.

## Create a new organization

If you have access you can create a new organization.

![organization-create](../../../../content/images/dashboard/orgs/create.png)

## Selecting an organization

Users can be members of multiple organizations,
you can visit your organization's dashboard to stay updated on recent activity and keep track of recent changes.

![organization-select](../../../../content/images/dashboard/orgs/select.png)

## Organization overview

Every organization can manage Projects, a Model Registry, and a Component Hub.

![organization-overview](../../../../content/images/dashboard/orgs/overview.png)

## Organization settings

The organization settings page provides several tabs to manage the account, members, teams, agents, connections, ...

![organization-settings-select](../../../../content/images/dashboard/orgs/settings-select.png)

The general settings page lets you change the organization's details

![organization-settings](../../../../content/images/dashboard/orgs/settings.png)

## Organization auth management

By default, users can join your organization by invitation only using username, email, and password.

In order to enable other authentication backends or open your organization for users without an invitation, you can use the auth tab in the settings

![organization-auth-settings](../../../../content/images/dashboard/orgs/auth-settings.png)

> **Note**: In Polyaxon Cloud, users can only join using a valid invitation.

## Organization Management

An organization can be further tuned to reflect the kind of access and scale you want to achieve.

 * You can create and manage projects.
 * You can manage the component hub.
 * You can manage the model registry.
 * You can create and manage agents to isolate and scale your workload over multiple namespaces and clusters.
 * You can create and manage queues to set priorities, routing, and scheduling strategies.
