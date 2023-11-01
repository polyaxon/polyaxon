---
title: "Artifacts Versioning"
sub_link: "artifacts-versioning"
is_index: true
meta_title: "Polyaxon management - Artifacts Versioning"
meta_description: "Polyaxon allows to promote runs and related assets to an artifact version."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="info">This feature is still in Beta!</blockquote>

## Overview

Polyaxon users can use their projects to promote and lock their runs to artifact versions, such projects provide:
 * APIs and a UI.
 * It can be used with your teams' configuration and access control settings to enable collaborative asset management.
 * Logging and lineage using the experimentation feature.
 * Versioning.
 * Requesting asset versions using fully qualified names.
 * Deploying as an internal tool or as a test API using the service abstraction.
 * Agnostic to the stored artifacts.

![overview](../../../../content/images/dashboard/artifacts-versioning/overview.png)

## Understanding artifacts versioning

Each project can have multiple artifact versions.

Each project can list all versions, their stage, their linked assets, their specification, and current usage.

Polyaxon provides a special tag to signal the stage of the artifact versions.

## Managing and using artifacts versioning

You can create and manage artifacts versions using the API, CLI or the dashboard.

Each artifact version can lock a run based on its id, and it can attach additional metadata.
By using `:tag`, you can add new versions to a project, Polyaxon uses the `owner/project-name` as a namespace.

## Usage

As soon as a artifact version is registered in a project,
you can use API/SDK to query information about it and use that information to deploy or request specific versions.
