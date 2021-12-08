---
title: "Organization Concepts"
sub_link: "concepts/organization-concepts"
meta_title: "Polyaxon Organization/Teams/Users - Core Concepts"
meta_description: "Polyaxon relies on a set of concepts to manage your organization, teams, and members."
visibility: public
status: published
tags:
  - architecture
  - concepts
  - polyaxon
sidebar: "intro"
---

Polyaxon relies on a set of concepts to manage your organization, teams, and members.
In this section, we provide a high-level introduction to these concepts,
with more details in pages dedicated to each concept.


### User

A `User` is the entity that creates projects, starts experiments, creates jobs and pipelines, manages teams and clusters.

<blockquote class="light">Please refer to <a href="/docs/management/organizations/user-profile/">management/users</a> for more details.</blockquote>

### Organization

An `Organization` is the entity that enables several users to collaborate across many projects at once.
Owners and managers can manage member access to the organization's data and projects with sophisticated security and administrative features. 
They can also delegate project, registry, and hub management to admins. 

<blockquote class="light">Please refer to <a href="/docs/management/organizations/">management/organizations</a> for more details.</blockquote>

### Team

A `Team` provides a way to manage groups of users, their access roles, and resources quotas and permissions.

<blockquote class="light">Please refer to <a href="/docs/management/organizations/teams/">management/teams</a> for more details.</blockquote>

### Project

A `Project` in Polyaxon is very similar to a project in GitHub,
it aims at organizing your efforts to solve a specific problem.
A project consists of a name and a description, access to several connections and data, and components to execute.

<blockquote class="light">Please refer to <a href="/docs/management/projects/general/">management/projects</a> for more details.</blockquote>

### Model Registry

A `Model` in Polyaxon is a format for packaging and managing machine learning models. This format is used to deploy these models using a variety of tools and technologies.

A `Model Registry` is a centralized model store, set of APIs, and UI, to collaboratively manage the full lifecycle of a model.
Users can promote an experiment to the model registry, and define information required for deploying the model using one or several frameworks.
A model in the registry can be traced back and reproduced easily using the lineage defined in the original experiment.

<blockquote class="light">Please refer to <a href="/docs/management/model-registry/">management/model-registry</a> for more details.</blockquote>

### Component Hub

A `component` is the model that describes the discrete and containerized logic you want to run,
they optionally take inputs, perform some work, and optionally return some outputs.

A `Component Hub` is a centralized store, set of APIs, and UI, to collaboratively manage the reusable components within an organization.
Users can always define components in their repos, and optionally when a component matures, they can promote it to the Component Hub.

<blockquote class="light">Please refer to <a href="/docs/management/component-hub/">management/component-hub</a> for more details.</blockquote>
