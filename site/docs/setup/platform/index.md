---
title: "Install Polyaxon on Kubernetes"
title_link: "Install Polyaxon on Kubernetes"
sub_link: "platform"
date: "2018-10-01"
meta_title: "How to install Polyaxon on Kubernetes"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon deployment using Kubernetes."
tags:
    - setup
    - kubernetes
    - install
sidebar: "setup"
---

<blockquote class="warning">
The open-source distribution for this version is not published yet! Please join the <a href="/slack/">chat</a> for more details.
</blockquote>

If you are here, it means that you have a Kubernetes cluster and [helm](/docs/guides/setup-helm/) setup.

This section include guides to deploy:
 * Polyaxon [Open Source](/docs/setup/platform/open-source/).
 * Polyaxon [EE Control Plane](/docs/setup/platform/control-plane/).
 
Both deployments share some [common Helm options](/docs/setup/platform/common-reference/). 

Please consider reading the other configuration sections to have a deeper knowledge about how to configure and customize Polyaxon to your need..

If you are deploying Polyaxon in production mode, you should take some time to read about some [best practices](/docs/guides/best-practices-for-deploying-polyaxon/) when deploying Polyaxon.

> **Tip**: The full list of the default [values.yaml](https://github.com/polyaxon/polyaxon-chart/blob/master/polyaxon/values.yaml)

## Create a namespace for Polyaxon

Polyaxon is deployed and uses a namespace to run operations
independently of other applications running on your cluster, we recommend using `polyaxon`.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

If you would like to use a different value, you must keep im mind to update the `namespace` value in your config.

## Configuration

This section will help you create a configuration file to deploy Polyaxon.
Polyaxon ships with [default values](/docs/setup/platform/reference/), however and depending on your use case
you might need to override some of these values.
To do so, you need to create a configuration file and we recommend to save it somewhere safe so that you can reuse it in the future.

Create a config file `config.yaml` or `polyaxon_config.yaml`,
and set up all information you want to override in the default config.

Example, adding database persistence

```yaml
postgresql:
  persistence:
    enabled: true
    size: 5Gi
```

## Install Polyaxon

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

Now you can install Polyaxon with your `config.yml` file

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

## Upgrade Polyaxon

To upgrade Polyaxon to a newer version, you can simply run the following command using Polyaxon CLI:

```bash
helm update
polyaxon admin deploy -f config.yml --upgrade
```

Or using Helm

```bash
helm update
helm upgrade polyaxon polyaxon/polyaxon -f polyaxon-config.yml
```

## Applying configuration changes

The general method to modify your Kubernetes deployment is to:

 1. Make a change to the config.yml
 2. [Optional] run `polyaxon admin deploy -f config.yml --check`
 2. Run a `polyaxon admin deploy -f config.yml --upgrade` or `helm upgrade`:

    ```bash
    $ helm upgrade <RELEASE_NAME> polyaxon/polyaxon -f config.yml
    ```

    Where `<RELEASE_NAME>` is the parameter you passed to `--name` when installing Polyaxon with `helm install`.

    If you don’t remember it, you can probably find it by doing `helm list`.

    If you used the default values suggested in the docs, the `<RELEASE_NAME>` should be `polyaxon`

  3. Wait for the upgrade to finish, and make sure that when you do
  `kubectl --namespace=<NAMESPACE> get pod` the pods are in Ready state.

    Your configuration change has been applied!


## Turn off Polyaxon

When you are done with Polyaxon, you can turn off the deployment,
and depending on your persistence configuration you can keep all your data saved for future deployments.

You can also decide to completely turn off Polyaxon and remove the namespace and computational resources.

`polyaxon admin teardown`

Or

`helm del --purge polyaxon`

### Stop/Delete running experiments/jobs

Polyaxon will by default stop all running jobs/experiments before a teardown, 
unless you prefer not to trigger the pre-delete hooks, in that case you should clean them on your own.  


### Delete Helm release

Delete the helm release. This deletes all resources that were created by helm during the deployment.

```bash
$ helm delete <RELEASE_NAME> --purge
```

If you used the default values, the command should be,

```bash
$ helm delete polyaxon --purge
```

If for some reason, your deployment did not succeed, 
you might need to delete Polyaxon with this command instead, to avoid triggering pre-delete hooks

```bash
$ helm delete polyaxon --purge --no-hooks
```

### Delete the namespace

Delete the namespace Polyaxon was installed in.
This deletes any disks that may have been created to store user’s logs|database,
and any IP addresses that may have been provisioned.

```bash
$ kubectl delete namespace <your-namespace>
```

If you used the default values, the command should be,

```bash
$ kubectl delete namespace polyaxon
```
