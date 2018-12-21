Polyaxon supports replication of the api and workers.

## Services Replication

To replicate the platform or one of the services (api or workers), you just need to modify `replicas` field of that service you want to scale.

For example to replicate `api`, your config yaml file should include:

```yaml
api:
  replicas: 3
```

This will create 3 pods for api to handle the traffic coming from the CLI, Dashboard, or REST API.

The easiest way to replicate the platform is increase the `replicas` of all Polyaxon's services:

```yaml
api:
  replicas: 3

scheduler:
  replicas: 3

hpsearch:
  replicas: 3

eventsHandlers:
  replicas: 3

k8sEventsHandlers:
  replicas: 3

eventMonitors:
  replicas: 3
```

## Concurrency

Replication might be the easiest option to scale Polyaxon, 
but it comes at a memory cost, and it's not always the most efficient option, 
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
