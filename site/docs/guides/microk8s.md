---
title: "Install Polyaxon on Microk8s"
title_link: "Install Polyaxon on Microk8s"
sub_link: "Microk8s"
date: "2018-10-01"
meta_title: "How to install Polyaxon on Microk8s"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon deployment using Microk8s."
custom_excerpt: "This is a guide to assist you through the process of setting up a Polyaxon deployment using Microk8s."
featured: false
visibility: public
status: published
tags:
    - guides
    - kubernetes
author:
  name: "Polyaxon"
  slug: "polyaxon"
  website: "http://polyaxon.com"
  twitter: "polyaxonai"
  github: "polyaxon"
---

## Install Microk8s

To install [https://microk8s.io/](https://microk8s.io/), please run the following command:

```bash
sudo snap install microk8s --classic


sudo snap alias microk8s.kubectl kubectl


microk8s.start


microk8s.enable \
  dashboard \
  dns \
  gpu \
  ingress \
  metrics-server \
  prometheus \
  registry \
  storage

microk8s.kubectl config view --raw > ~/.kube/config
```

## Polyaxon configuration

If you are here, it means that you have a Microk8s cluster and [helm](/docs/guides/setup-helm/) setup.

Please consider reading our [configuration guides](/configuration/introduction/) to have a deeper knowledge about how to configure and customize Polyaxon to your need.

Please also check the [helm reference](/references/polyaxon-helm-reference/) for all default values.

Create a config file `config.yaml` or `polyaxon_config.yaml`,
and set up all information you want to override in the default config.


## RBAC

If you are not using Polyaxon with RBAC enabled you should disable it in your config.yaml file

```yaml
rbac:
  enabled: false
```

## Use a NodePort service

```yaml
serviceType: NodePort
``` 

## Create a namespace for Polyaxon

Polyaxon installs and uses a namespace to run experiments
independently of other applications running on your cluster, we recommend using `polyaxon`.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

If you would like to use a different value, you must keep im mind to update the `namespace` value in your config.

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

### Deploy

Now you can install Polyaxon with your `config.yml` file

You can use Polyaxon CLI to manage the deployment

```bash
polyaxon admin deploy -f config.yml
```

Or you can use Helm to do the same:

```bash
helm install polyaxon/polyaxon \
    <RELEASE_NAME> \
    --namespace=<NAMESPACE> \
    -f config.yml
```

`<RELEASE_NAME>` is an identifier used by helm to refer to this deployment.
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


## Env var for setting the CLI

```bash
set -xg POLYAXON_PORT (kubectl get --namespace polyaxon -o jsonpath="{.spec.ports[0].nodePort}" services polyaxon-polyaxon-api)
set -xg POLYAXON_IP (kubectl get nodes --namespace polyaxon -o jsonpath="{.items[0].status.addresses[1].address}")

env | grep POLYAXON

echo http://$POLYAXON_IP:$POLYAXON_PORT

polyaxon config set --host=$POLYAXON_IP --port=$POLYAXON_PORT
```

## Upgrade Polyaxon

To upgrade Polyaxon to a newer version, you can simply run the following command using Polyaxon CLI:

```bash
polyaxon deploy -f config.yml --upgrade
```

Or using Helm

```bash
helm upgrade polyaxon polyaxon/polyaxon -f config.yml
```

## Applying configuration changes

The general method to modify your Kubernetes deployment is to:

 1. Make a change to the config.yml
 2. [Optional] run `polyaxon deploy -f config.yml --check`
 2. Run a `polyaxon deploy -f config.yml --upgrade` or `helm upgrade`:

    ```bash
    $ helm upgrade <RELEASE_NAME> polyaxon/polyaxon -f config.yml
    ```

    Where `<RELEASE_NAME>` is the parameter you passed to `--name` when installing Polyaxon with `helm install`.

    If you don’t remember it, you can probably find it by doing `helm list`.

    If you used the default values suggested in the docs, the `<RELEASE_NAME>` should be `polyaxon`

  3. Wait for the upgrade to finish, and make sure that when you do
  `kubectl --namespace=<NAMESPACE> get pod` the pods are in Ready state.

    Your configuration change has been applied!

## Issues

### DNS issues

If the dns isn't reflected from the host to the pod. Please run:
```bash
sudo iptables -P FORWARD ACCEPT
```

This could solved the issue.


### Build failure

If your builds using the native dockerizer are not succeeding, please use kaniko as build process.


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
