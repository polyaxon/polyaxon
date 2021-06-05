---
title: "Managing and exposing a catalog of machines"
sub_link: "scheduling-presets/machines-catalog"
meta_title: "Organizing your cluster(s) as a catalog of machines or environments - scheduling presets"
meta_description: "By combining Queues and Presets, users can expose their cluster(s) as an organized and easy-to-use catalog of machines."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

By combining Queues and Presets, users can expose their cluster(s) as an organized and easy-to-use catalog of machines or environments.

> **Note**: In this guide we will use the terms environments, machines, and instances interchangeably to refer to the same concept.    

## Using queues in presets

Sometimes it's useful to combine the environment section, container resources, and queues to set priority and/or concurrency for accessing environments, specific hardware, or machines.

Presets provide the abstraction to combine these notions into a simple reference.
Let's look again at the example where we would like to expose a large instance machine to the end-users, but only allow running two instances at the same time.

We first need to create a queue on the agent where we would like to expose the GPU instances. please see the [queues](/docs/management/organizations/queues/) management section.
After creating the queue, we can include it in the preset definition.

```yaml
queue: agent-name/queue-with-2-concurrency
runPatch:
  environment:
    nodeSelector:
      node_label: gpu-experiments
  container:
    resources:
      limits:
        nvidia.com/gpu: 4
```  

![instance-creation](../../../../content/images/dashboard/instances/instance-creation.png)

By [saving this preset](/docs/management/organizations/presets/) as `4-gpus-2-concurrency-machine`.
Users can now queue runs to use the large instance environment and only allow 2 concurrent operations at any given time:

```bash
polyaxon run ... --presets=4-gpus-2-concurrency-machine
```

You can also use the preset directly on the component or operation definition:

```yaml
kind: operation
presets: [4-gpus-2-concurrency-machine]
...
```

By using your presets you can create a catalog of machines or environments with resources requests, priority and concurrency limits.

## Best practices for creating a catalog of environments

![catalog-management](../../../../content/images/dashboard/instances/catalog-management.png)

To create a new preset, you should go under `organization > settings > presets`:

 * Name: We suggest that you give an easy name that reflects to the type of the environment/machine/instance, with suffixes about priority and or concurrency, e.g. `large-gpu-max-concurrency-2`, the name could also signal if an instance is an on-demand/spot instance.
 * Description: This field is also visible directly on the presets table and should give your users a clear idea about what the preset does.
 * Tags: In order to differentiate between presets that will be used for the catalog and other presets that could be used for other use-cases, we suggest defining and using tags. Users will be able to filter the presets table by tags, e.g. `tags: [machines]` or `tags: [instances, spot]`.
 * Definition: this is where you set your preset definition with information about resources, queue, node scheduling, ...


## Guidance on preset definition

The preset definition can include several information, and you can use the same definition several times in different presets instances. 

For example: 
 * You can define a preset that schedules a type of GPU machine or environment.
 * You can also add the same preset, but with priority or concurrency.
 * You can also define the same preset with a termination policy, e.g. a default timeout of 4h, anyone using this preset cannot run a job for more than 4 hours.
 * You can define the preset with various base images, e.g. `tensorflow:2.3.2`. 

## End-user interaction with presets

Data scientists and ML engineer who do not have `owner` or `manager` cannot create or edit presets, they only have access to a catalog of machines to use:

![catalog-view](../../../../content/images/dashboard/instances/catalog-view.png)

Based on tags and description they can see the definition how to use the preset:

![instance-usage](../../../../content/images/dashboard/instances/instance-usage.png)


## Setting the default machine/instance/environment preset

In some use case project admin might need to configure a default machine/instance/environment to use for a specific project, 
or to predefine a scheduling preset to be used by default when running operations in the context of a specific project.

Polyaxon provides a configuration under the project's settings to configure the default preset:

![default-instance](../../../../content/images/dashboard/instances/default-instance.png)

## Restricting accessible presets in a specific project

Sometimes it's useful to restrict the instances that users can reference in their component/operation specification to use in the context of a specific project.

Polyaxon provides a configuration under the project's settings to configure the accessible presets:

![accessible-instances](../../../../content/images/dashboard/instances/accessible-instances.png)
