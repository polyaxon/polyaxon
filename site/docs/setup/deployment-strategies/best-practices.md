---
title: "Deployment Best Practices"
sub_link: "deployment-strategies/best-practices"
title_link: "Deployment Best Practices"
meta_title: "Deployment Best Practices"
meta_description: "Deploying Polyaxon can be hard, not only because it requires using Kubernetes a tool that is hard to manage and maintain, but also because it is a stateful application. In this guide, we will try to go through several aspects of Polyaxon deployment that we think any user trying to use Polyaxon in production mode should think about."
tags:
  - setup
  - kubernetes
  - install
sidebar: "setup"
---

In this guide, we will try to go through several aspects of Polyaxon deployment that we think any user trying to use Polyaxon in production mode should think about.

Polyaxon uses Kubernetes, a tool that is rapidly getting adopted by several teams, but running stateful application on Kubernetes could be hard.

## Scheduling

Polyaxon depends on some core components to function correctly, these core components include the API, the scheduler, other helper services,
and third party services like a database for example. In addition to these core components, Polyaxon schedules jobs and experiments that data scientists submit to the platform.

In order to keep the core components highly responsive, we recommend that users should deploy them on separate nodes than those used for running the user's workload.
This ensures that experiments, jobs, dashboards, and apps, won't consume CPU and/or memory that could be essential to the database or the API to be responsive.

In order to achieve such behavior, please check:
 * The [node and deployment manipulation](/docs/setup/platform/common-reference/#node-and-deployment-manipulation/) section to configure its core services.
 * The [node scheduling](/docs/core/scheduling-strategies/node-scheduling/) section to configure scheduling for the data scientist's workload.
 * The [presets](/docs/core/scheduling-presets/) section to create common configuration for your experiments, jobs, builds, scheduling, resources requesting, and other use-cases you need to solve.

You can also decide to just use at a minimum 2 selectors one for core components and one for the workload to keep them separated.

Several teams have advanced setups where they take advantage of Node Selectors, Affinity, and Tolerations to setup the default platform behavior,
and use a custom scheduling per experiment/job when needed. Please refer to this section for a full reference of the [node scheduling behavior](/docs/setup/platform/common-reference/#node-and-deployment-manipulation).

If you are running Polyaxon Enterprise Edition, you can also deploy the control plane in a separate namespace or even cluster than the data plane(workloads)

> **Note**: make sure that Polyaxon's dependencies are not deployed on the same node where you are running your experiments and jobs,
> this way you won't impact the stability of these components if one of the runs has a high CPU/Memory consumption or being preempted.

## Database high availability

If you are running Polyaxon in production mode, we suggest that you keep your database "safe" and highly available.
We provide a reference document on how to achieve High Available Database on Polyaxon in this [guide](/docs/setup/platform/postgresql-ha/).

Stateful applications are very hard to set up correctly on a Kubernetes cluster, so to achieve Postgres HA, we suggest that you look at setting an external Database with Polyaxon.

We also recommend users to take snapshots and backups before going through a migration, this is particularly important if an upgrade contains DB or Data migrations.

> **Note**: We strongly recommend that you do not deploy a production database using this chart. Although the provided database can persist data if configured, 
> you might encounter an issue in the future if we upgrade the dependency requirements or the version of the database image changes.

## Other components high availability

If you are running Polyaxon in production mode and using a scheduler, you might think about using a managed version of one or several dependencies. please check:

 * [redis](/docs/setup/platform/redis-ha/).
 * [rabbitmq](/docs/setup/platform/rabbitmq-ha/).

## Storages

Your experiments' and jobs' outputs, logs, models, and artifacts should be stored using a highly available storage backend.

In order to enable durable, i.e. available after a node failure, we recommend that you read the following guides: [artifacts store](/docs/setup/connections/artifacts/).

Polyaxon supports several artifacts stores for your on-premise or cloud deployment.

If you are using Polyaxon EE or Polyaxon Cloud you can deploy several agents backed by different artifacts stores depending on your requirements.

> **Note**: The default configuration uses a temporary storages

## SSL & Network Security

Security is important and we strongly recommend that you deploy Polyaxon on a network that you control.
If you expose the gateway to the internet we recommend that you use SSL for your Polyaxon deployment.

Please read this [SSL reference](/docs/setup/platform/common-reference/#ssl),
our [FAQ on using custom domain](/faq/use-custom-domain/),
[Nginx Ingress](/integrations/nginx/),
and [Let's encrypt](/integrations/letsencrypt/).

If you can't deploy Polyaxon with SSL or if you don't control the network,
we suggest that you keep the default network configuration: `ClusterIP` and use port forwarding to access Polyaxon API and UI.
Please check this [section](/docs/setup/platform/#port-forward) for more details.

## Security context

Starting from Polyaxon v0.5, we recommend running all Polyaxon's services and workloads with a non-root/privileged user.

Polyaxon exposes a security context to setup a user uid and a group gid to use for its containers.

All mounted volumes will have a filesystem group with the same value as the gid provided by the user.
Please check this [section](/docs/setup/platform/common-reference/#security-context) for more details.
