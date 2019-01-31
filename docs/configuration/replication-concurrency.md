---
title: "Replication & Concurrency"
sub_link: "replication-concurrency"
meta_title: "Replication and Concurrency in Polyaxon - Configuration"
meta_description: "Polyaxon supports scaling of it's services (api and workers) in horizontal way using replication, and the user can increase the workers' concurrency for higher throughput."
tags:
    - configuration
    - polyaxon
    - replication
    - scaling
    - concurrency
    - kubernetes
    - docker-compose
sidebar: "configuration"
---

Polyaxon supports scaling of it's services (api and workers) in horizontal way using replication, and the user can increase the workers' concurrency for higher throughput.

## Services Replication

To replicate the platform or one of the services (api or workers), you just need to modify the `replicas` field of that service you want to scale horizontally.

For example to replicate `api`, your config yaml file should include:

```yaml
api:
  replicas: 3
```

This will create 3 pods for api to handle the traffic coming from the CLI, Dashboard, or REST API.

The easiest way to replicate the platform is to increase the `replicas` of all Polyaxon's services:

```yaml
api:
  replicas: 3

scheduler:
  replicas: 3

hpsearch:
  replicas: 3

eventsHandlers:
  replicas: 3

eventMonitors:
  replicas: 3
```

## Concurrency

Replication might be easier to scale Polyaxon, but it comes at a memory cost, as it's not always efficient, 
Polyaxon provides a way to scale it's services' concurrency as well, 
the rule of thumb is to set the concurrency of the worker you wish to scale to the number of cores available. 
This will allow to reduce the memory footprint on your cluster and allow the worker to consume more events/tasks.

For example you may want to increase the concurrency of the scheduler:

```yaml
scheduler:
  replicas: 2
  concurrency: 10  
``` 

This will create 2 replicas for the scheduler, with 10 concurrent processes each.


## Resources' limit

By default Polyaxon does not set limits on the resources for the core components it deploys,
in order to enable the resources limits, your config yaml file should include:

```yaml
limitResources: True
```

This will force the Polyaxon to set the resources limits on all services if they include the limits subsections.
