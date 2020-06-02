---
title: "Polyaxon deployment best practices"
title_link: "Polyaxon deployment best practices"
meta_title: "Polyaxon deployment best practices"
meta_description: "Deploying Polyaxon can be hard, not only because because it requires using Kubernetes a tool that is not yet fully used by several teams, but also because it is a stateful application."
custom_excerpt: "Deploying Polyaxon can be hard, not only because because it requires using Kubernetes a tool that is not yet fully used by several teams, but also because it is a stateful application."
featured: true
author:
  name: "Polyaxon"
  slug: "polyaxon"
  website: "http://polyaxon.com"
  twitter: "polyaxonai"
  github: "polyaxon"
visibility: public
status: published
tags:
    - tutorials
---

In this guide we will try to go through several aspects of Polyaxon deployment that we think any user trying to use Polyaxon in production mode should think about.

Polyaxon uses Kubernetes, a tool that is rapidly getting adopted by several teams, but running stateful application on Kubernetes could be hard.

## Scheduling

Polyaxon depends on some core components to function correctly, these core components include the API, the scheduler, other services for hptuning and for monitoring, 
and third party services like a database for example. In addition to these core components, Polyaxon schedules jobs and experiments for every data scientist using the platform.

In order to keep the core components highly responsive, we recommend that users should deployed them on separate nodes than those used for running user's workload. 
This ensures that, experiments and jobs won't consume CPU and/or memory that could be essential to the database or the API to be responsive.

In order to achieve such behaviour Polyaxon provides a [node scheduling configuration](/configuration/custom-node-scheduling/).

Here's an example of the minimum requirement that we suggest for a production cluster:

```yaml
nodeSelector:
  core:
    polyaxon: core
  experiments:
    polyaxon: experiments
  jobs:
    polyaxon: experiments
  builds:
    polyaxon: builds
  tensorboards:
    polyaxon: experiments
```

You can also decide to just use at a minimum 2 selectors one for core components and for the workload to keep them separated.

Several teams have advanced setup where they take advantage of Node Selectors, Affinity, and Tolerations to setup the default platform behaviour, 
and use a custom scheduling per experiment/job when needed. Please refer to this section for full reference of the [node scheduling behaviour](/configuration/custom-node-scheduling/).

> N.B. make sure that Polyaxon's dependencies are not deployed on the same node where you are running your experiments and jobs, 
this way you won't impact the stability of these components if one of the runs has a high CPU/Memory consumption or being preempted.

## Database high availability

If you are running Polyaxon in production mode, we suggest that you keep your database "safe" and highly available. 
We provide a reference document on how to achieve High Available Database on Polyaxon in this [guide](/docs/setup/platform/postgresql-ha/).

Stateful application are very hard to setup correctly on a Kubernetes cluster, so to achieve Postgres HA, we suggest that to look at setting an external Database with Polyaxon.

We also recommend users to take snapshots and backups before going through a migration, this is particularly important if an upgrade contains DB or Data migrations.

## Other components high availability

If you are running Polyaxon in production mode and using a cloud provider, you might think about using a managed version of one or several dependencies. please check:

 * [redis](/docs/setup/platform/redis-ha/).
 * [rabbitmq](/docs/setup/platform/rabbitmq-ha/).

## Storages

Your experiments and jobs outputs/artifacts and logs are stored by default in temporary storages, in order to enable durable, i.e. available after a node failure, we recommend that you read the following guides:
  * [artifacts store](/docs/setup/connections/artifacts/)

## SSL

Security is important and we strongly recommend that you use SSL for your Polyaxon deployment, please read this [SSL reference](/configuration/ssl/), 
our [FAQ on using custom domain](/faq/use-custom-domain/), [Nginx Ingress](/integrations/nginx/), and [Let's encrypt](/integrations/letsencrypt/). 

## Security context

Starting from Polyaxon v0.5, we recommend running all Polyaxon's services and workloads with a non-root/privileged user.

Polyaxon exposes a security context to setup a user uid and a group gid to use for it's containers.

All mounted volumes will have a filesystem group with the same value as the gid provided by the user. 

## Debugging

Debugging workloads on Kubernetes can be challenging, we generally tell our users:

 * to start a notebook to get an interactive environment to try their code
 * to try their code locally first, before submitting long running jobs to Polyaxon
 * Take advantage of local run `polyaxon run ... --local`

For our tracking API, Polyaxon respect a setting to [disable calls to the APIs](/docs/experimentation/tracking/#disabling-polyaxon-tracking-without-changing-the-code).

We are also in the process of providing Local Runs for Polyaxon, where user will be able to generate dockerfiles locally, run them, and track the result similar to the in-cluster behaviour.


