---
title: "Install Polyaxon on Minikube"
title_link: "Install Polyaxon on Minikube"
sub_link: "Minikube"
date: "2018-10-01"
meta_title: "How to install Polyaxon on Kubernetes"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon deployment using Kubernetes."
tags:
    - guides
    - kubernetes
---

If you are here, it means that you have a Minikube cluster and [helm](/docs/guides/setup-helm/) setup.

Please consider reading our [configuration guides](/configuration/introduction/) to have a deeper knowledge about how to configure and customize Polyaxon to your need.

Please also check the [helm reference](/references/polyaxon-helm-reference/) for all default values.

## Minikube resources

For [Minikube](https://github.com/kubernetes/minikube), we recommend Virtualbox/VMware drivers, but you can also use other drivers.

We recommend also to increase the amount of resources allocates:

```bash
minikube start --cpus 4 --memory 8192 --disk-size=40g
```

By default Minikube allocates 2Gb of RAM, this not enough for Polyaxon and we recommend at least 6Gb.

## RBAC

If you are using Polyaxon with RBAC enabled, you should add the following option:

```bash
--extra-config=apiserver.authorization-mode=RBAC
```

## Create a namespace for Polyaxon

Polyaxon installs and uses a namespace to run experiments
independently of other applications running on your cluster, we recommend using `polyaxon`.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

If you would like to use a different value, you must keep in mind to update the `namespace` value in your config.

## Configuration

This section will help you create a configuration file to deploy Polyaxon.
Polyaxon ships with [default values](/references/polyaxon-helm-reference/), however and depending on your use case
you might need to [override](/configuration/introduction/) some of these values.
To do so, you need to create a configuration file and we recommend to save it somewhere safe so that you can reuse it in the future.

Create a config file `config.yaml` or `polyaxon_config.yaml`,
and set up all information you want to override in the default config.

### Set Minikube deployent type

First thing to update your `polyaxon_config.yaml` is your deployment type:

```yaml
deploymentType: minikube
```

### Disabling RBAC and ingress


By default Polyaxon uses LoadBalancer and RBAC, you might need to disable one / both of them in your `config.yml`/`polyaxon_config.yml`:

```yaml
deploymentType: minikube

rbac:
  enabled: false

ingress:
  enabled: false

serviceType: NodePort
```

It is however recommended to enable RBAC and start minikube with the option `--extra-config=apiserver.authorization-mode=RBAC`.


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
    --name=<RELEASE_NAME> \
    --namespace=<NAMESPACE> \
    -f config.yml
```

`--name` is an identifier used by helm to refer to this deployment.
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

### Minikube IP

After installing polyaxon, you might need to use the following command to enable access to the API service:

```bash
minikube service -n polyaxon polyaxon-polyaxon-api
```

Note that when using minikube, the IP address of the application is given by `minikube ip`.

These notes are important for setting the CLI, and getting access to the dashboard.

Next step you need the [Polyaxon CLI installed](/docs/setup/cli/), and you need to configure 
the host and the ports based on these notes.

## Upgrade Polyaxon

To upgrade Polyaxon to a newer version, you can simply run the following command using Polyaxon CLI:

```bash
polyaxon admin upgrade -f config.yml
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
