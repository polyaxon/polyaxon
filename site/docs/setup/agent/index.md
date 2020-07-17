---
title: "Install Polyaxon Agent on Kubernetes"
title_link: "Install Polyaxon Agent on Kubernetes"
sub_link: "agent"
is_index: true
meta_title: "How to install Polyaxon Agent on Kubernetes"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon Agent deployment using Kubernetes."
tags:
    - setup
    - kubernetes
    - install
sidebar: "setup"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

If you are here, it means that you have access to a Polyaxon EE Control Plane or Polyaxon Cloud.

## Overview 

![polyaxon agent](../../../../content/images/references/agent/agent-operator.png)

 * Agents interact with Polyaxon Control Plane to check the queues that they manage for operations to start, stop, or update.
 * Agents can deploy different artifacts store and connections to ensure isolation, it's also possible to deploy similar configurations on different clusters to enable access to new resources, e.g. on-prem GPU and GKE for TPUs. 
 * Agents can be used to only deploy jobs / distributed jobs workload, and they can also deploy and expose services.

It's important to note that Polyaxon Agent is an important piece in Polyaxon architecture to enable complete isolation and a hybrid execution.

![polyaxon agent](../../../../content/images/references/agent/agent-execution.png)

## Create a namespace for the agent

Agents are deployed and use a namespace to run operations
independently of other applications running on your cluster.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

If you would like to use a different value, you must keep in mind to update the `namespace` value in your config.

## Configuration

This section will help you create a configuration file to deploy an agent.
Polyaxon Agent ships with [default values](/docs/setup/agent/reference/), however and depending on your use case
you might need to override some of these values.
To do so, you need to create a configuration file and we recommend to save it somewhere safe so that you can reuse it in the future.

Create a config file `config.yaml` or `polyaxon_config.yaml`,
and set up all information you want to override in the default config.

If you are using Polyaxon CLI to deploy Polyaxon, we suggest that you define the version and deployment type:

```yaml
deploymentChart: agent
deploymentVersion: 1.1.0
```

In Polyaxon UI you can get an starter deployment config:

![agent-deployment](../../../../content/images/dashboard/agents/deployment.png)

> To manage agents please check the [management section](/docs/management/ui/agents/)

## Install Polyaxon Agent

First of all, you need to [add](https://github.com/kubernetes/helm/blob/master/docs/chart_repository.md) the [Polyaxon helm repository](https://charts.polyaxon.com/)
to your helm, so you can install Polyaxon from it.
This makes it easy to refer to the Polyaxon chart without having to use a long URL each time.

```bash
helm repo add polyaxon https://charts.polyaxon.com
helm repo update
```

### Validate
 
You can validate that your deployment `config.yml` file is compatible with the version you are trying to deploy:

```bash
polyaxon admin deploy -f config.yml --check
```

### Dry run

To perform a dry run:

```bash
polyaxon admin deploy -f config.yaml --dry_run
```

### Deploy

Now you can install Polyaxon Agent with your `config.yml` file.

> **Note**: it's important to know that there's an initial delay before you can access Polyaxon API, and before some pods will turn green, which is set to 2 minutes. 

You can use Polyaxon CLI to manage the deployment

```bash
polyaxon admin deploy -f config.yml
```

Or you can use Helm to do the same:

in Helm 2

```bash
helm install polyaxon/polyaxon \
    --name=<RELEASE_NAME> \
    --namespace=<NAMESPACE> \
    -f config.yml
```

in Helm 3

```bash
helm install <RELEASE_NAME> polyaxon/polyaxon \
    --namespace=<NAMESPACE> \
    -f config.yml
```

`--name` or `name` is an identifier used by helm to refer to this deployment.
You need it when you are changing the configuration of this install or deleting it.
We recommend using `RELEASE_NAME = polyaxon` or `RELEASE_NAME = plx`.

`--namespace` should be the same value of the namespace you created in the first step,
we again recommend using `polyaxon` to make it always easy to remember.

> **Tip**: We recommend using `polyaxon` for both the `--name` and `--namespace` to avoid too much confusion.
> The same command with `polyaxon` as a value:

```bash
helm install polyaxon/polyaxon \
--name=polyaxon \
--namespace=polyaxon \
-f config.yml
```

>**Note**: "Release name already exists error"
> If you get a release named `<RELEASE_NAME>` already exists error, then you should delete the release by running `helm delete --purge <RELEASE_NAME>`.

You can see the pods being created by entering in a different terminal:

```bash
kubectl --namespace=<NAMESPACE> get pod
```

When helm is done deploying Polyaxon, it will output some instructions `NOTES`,
these note will be different depending on your configuration (the service type used and/or ingress);

```
NOTES: ...
```

These notes are important for setting the CLI, and getting access to the dashboard. 

Next step you need the [Polyaxon CLI installed](/setup/cli/), and you need to configure 
the host and the ports based on these notes.

## Upgrade Polyaxon Agent

To upgrade Polyaxon to a newer version, you can simply run the following command using Polyaxon CLI:

```bash
polyaxon admin upgrade -f config.yml
```

Or using Helm

```bash
helm upgrade polyaxon polyaxon/polyaxon -f config.yml
```

## Turn off a Polyaxon Agent

When you are done with an agent, you can turn off the deployment,
and depending on your persistence configuration you can keep all your data saved for future deployments.

You can also decide to completely turn off Polyaxon and remove the namespace and computational resources.

`polyaxon admin teardown -f config.yml`

Or

`helm del --purge polyaxon`

You can also delete the [agent from the dashboard](/docs/management/ui/agents/).

### Delete the namespace

Delete the namespace the agent was installed in.
This deletes any disks that may have been created to store user’s logs,
and any IP addresses that may have been provisioned.

```bash
$ kubectl delete namespace <your-namespace>
```

If you used the default values, the command should be,

```bash
$ kubectl delete namespace polyaxon
```
