---
title: "Model Registry"
sub_link: "model-registry"
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

Polyaxon users can use turn a project to provides a model registry, such project provides:
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

Each model can list all versions, their stage, their model artifacts used, their specification, and their metrics and current usage.

Polyaxon provides a special tag to signal the stage of your models' versions.

## Managing and using models

You can create and manage models and versions using the API, CLI or the dashboard.

> Please check the model management guide. 

Each model version uses can lock an experiment run based on its id, it can have metadata, and framework.
By using `:tag`, you can add new versions to a model registry, Polyaxon uses the `owner/model-name` as a namespace for each model.

> Please check the model version management guide.

## Usage

As soon as a model is registered in your organization's registry, 
you can use API/SDK to query information about your model and use that information to deploy specific versions.

At the moment the model registry is accessible to all organization for locking experiment runs, and for organizing candidate models and their lifecycle.

Some customers have access to the monitoring and the post-deployment events API, which should be opened to everyone as soon as the events interface is finalized.   
