---
title: "Migration to v1.x"
sub_link: "migration"
meta_title: "Migration to Polyaxon v1.x - Polyaxon Releases"
meta_description: "Polyaxon Migration to Polyaxon v1.x."
visibility: public
status: published
tags:
    - reference
---

> **Important**: Polyaxon v1 is not backward compatible with Polyaxon v0, this guide is for the community edition's users.

This is a WIP guide for manually migrating your Polyaxon CE deployment from v0 to v1.

## Polyaxonfiles

The Polyaxonfile specification has several changes:
 * Support standard Kubernetes container and pod sections: all custom `cmd`, `resources`, and `node selectors` are now using standard Kubernetes definitions.
 * Camel case vs Snake case: the full specification is now camel case to make it easier for people to use snippets from guides and resources in the Kubernetes world and use them in Polyaxon.
 * Two main primitives: `Component` and `Operation`, the runtime defines how an operation is compiled and executed:
   * Single job abstraction for managing jobs, builds, and experiments.
   * Single service abstraction for managing: notebooks, Tensorboards, VSCode, Streamlit, Voila, ...

## Apis, Clients, & CLI

We removed all specific APIs and commands for: `experiments`, `jobs`, `builds`, `notebooks`, `tensorboards`,
and consolidated all logic under the `/api/v1/{owner}/{project}/runs` endpoints and `polyaxon ops` commands group.

The CLI and Client have also a single function for starting jobs, services, experiments, and dags:
 * `polyaxon run ...`
 * `client.create_ ...`

## Customizable plugins

Issues related to Tensorboard and Notebook can be solved by users themselves without waiting for new releases. Polyaxon provides several public components,
but users can customize them at any point.

It's still possible to start Tensorboard and Notebook in a simple way, e.g.:

 * `polyaxon run --hub tensorboard:version`

## Helm & deployment

 * The built-in docker registry is removed: users can still deploy an in-cluster registry for managing docker images,
   but the behavior is now standardized across all registry providers.
 * Celery Scheduler is disabled by default: which means no dependency on Redis or Rabbitmq unless the scheduler is enabled, and only one dependency is required.
 * Git is managed through external providers by default: no volume for managing repos is required anymore.
 * Logs and outputs are managed through a single artifacts store: One artifacts store connection to manage logs, events, and outputs.

## Connections

All integrations with external systems are managed using the `Connection` abstraction.

Connections are how Polyaxon connects users' workload with artifacts stores, data stores,
notification providers, git providers, registry providers, ssh connections, database connections, ...

Connections have a simple and generic schema for managing secrets and config maps.

 * You can expose S3/GCS/Azure using the standard way that is used in other systems or using the default CLIs, Polyaxon does not require any special changes.
 * Integration with docker/container registries follows standard definitions for mounting secrets and config maps: any tutorial found on the internet for mounting some specific registry should work on Polyaxon.
 * Polyaxon also integrates with several other connections, and users can define custom behavior for consuming connections since they are just mounting secrets and config-maps.

## Auth and User management

Polyaxon CE is now very easy to deploy, and does not provide an auth system:
 * Users in Polyaxon CE can access all projects, submit jobs, and view shared results under a single organization.
 * Polyaxon CE users can achieve namespacing using Projects or using multiple Polyaxon CE deployments.
