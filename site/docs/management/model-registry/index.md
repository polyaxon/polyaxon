---
title: "Model Registry"
sub_link: "models-registry"
is_index: true
meta_title: "Polyaxon management - Model Registry"
meta_description: "Polyaxon Model Registry is a powerful models store and a system to manage versioning, logging, staging, and production."
tags:
    - concepts
    - polyaxon
    - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>
<blockquote class="info">This feature is still in Beta!</blockquote>

## Model Registry

Polyaxon Model Registry is a models store and a system that provides:
 * APIs and a UI.
 * It can be used with your teams' configuration and access control settings to enable collaborative model management.
 * Logging and lineage using the experimentation feature.
 * Versioning.
 * Deploying as an internal tool or as a test API using the service abstraction.
 * Agnostic to the model packaging format.
 * Integrations with your favorite serving technologies.

![overview](../../../../content/images/dashboard/registry/overview.png)

## Understanding the model registry

Each model can have multiple versions.

![created-stage](../../../../content/images/dashboard/registry/created.png)

Each model can list all versions, their stage, their model artifacts used, their specification, and their metrics and current usage.

![production-stage](../../../../content/images/dashboard/registry/production.png)

Polyaxon provides a special tag to signal the stage of your components' versions.

![testing-stage](../../../../content/images/dashboard/registry/testing.png)

By default, the Component Hub shows the latest version and its stage.

![staging-stage](../../../../content/images/dashboard/registry/staging.png)

