---
title: "Queues"
sub_link: "ui/queues"
meta_title: "Polyaxon management tools and UI - Queues"
meta_description: "Polyaxon Queue manage, queue, route, prioritize, and throttle operations."
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

If you have admin access you can create new queues.

![queue-create](../../../../content/images/dashboard/queues/create.png)


## Manage queues

You can list, review, and manage all queues for each agent.

![queue-manage](../../../../content/images/dashboard/queues/manage.png)

## Queue settings

You can update or delete an queue.

![queue-settings](../../../../content/images/dashboard/queues/settings.png)
