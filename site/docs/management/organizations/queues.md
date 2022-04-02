---
title: "Queues"
sub_link: "organizations/queues"
meta_title: "Polyaxon management tools and UI - Queues"
meta_description: "Polyaxon manage, queue, route, prioritize, and throttle operations."
tags:
  - concepts
  - polyaxon
  - management
sidebar: "management"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

Polyaxon provides a queue abstraction to:
  * Prioritize operations on a queue.
  * Throttle the number of operations on a queue.
  * Route operations on a queue to a namespace or cluster.
  * Limit the number of operations queued from a single workflow or nested workflows.


Every agent comes with a default queue.

## Create queues

If you have admin access you can create new queues

![queue-create](../../../../content/images/dashboard/queues/create.png)

You can also attach a quota to a queue

![queue-create](../../../../content/images/dashboard/queues/create-quota.png)

> **Note**: The quota field accepts any resource format supported by Kubernetes e.g. (5Gi, 0.5m, 1000, ...)

## Manage queues

You can list, review, and manage all queues for each agent.

![queue-manage](../../../../content/images/dashboard/queues/manage.png)

## Queue settings

You can update or delete a queue.

![queue-settings](../../../../content/images/dashboard/queues/settings.png)

## Queues viewer

Users without admin or owner rights can view the table of available queues in your organization.

![queue-viewer](../../../../content/images/dashboard/queues/viewer.png)

## Queues usage

They can also view details on how to use them in their workload.

![queue-definition](../../../../content/images/dashboard/queues/definition.png)


## Global or per project queues

Managers and Admins of Polyaxon organizations and projects can set a default queue that gets applied to all runs under the organization or the project.

Setting the organization's default queue:

![default-org-preset](../../../../content/images/dashboard/queues/default-org-queue.png)

Setting a project's default queue:

![default-project-preset](../../../../content/images/dashboard/queues/default-project-queue.png) 

Restricting queues accessible by a project:

![default-project-preset](../../../../content/images/dashboard/queues/queues-restrictions.png)
