---
title: "Connections"
sub_link: "organizations/connections"
meta_title: "Polyaxon management tools and UI - Connections"
meta_description: "Polyaxon connection management."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

Polyaxon provides a connection abstraction to:
  * Access buckets and volumes.
  * Connect to databases and remote services.
  * Integrate Polyaxon with external services.
  * Subscribe Polyaxon to external events or notify external system with events in Polyaxon.

Connections are defined and managed on your clusters on-premise or you cloud clusters, and are managed by the team that manages your Kubernetes cluster and Polyaxon Agent deployments.

Polyaxon UI provides a nice viewer to summarise all the connections defined in your organization that you can sort by: kind, agent, dates, and other meta data. 
And provides instructions to your end-users on how they can request access and use these connection in their workload.   

## Connections viewer

All users can view the table of available connections in your organization.

![connections-viewer](../../../../content/images/dashboard/connections/viewer.png)

## Connections usage

And they can also view details on how to use them in their workload.

![connections-usage](../../../../content/images/dashboard/connections/usage.png)
