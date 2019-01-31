---
title: "Install Polyaxon on Kubernetes"
title_link: "Install Polyaxon on Kubernetes"
sub_link: "kubernetes"
date: "2018-10-01"
meta_title: "How to install Polyaxon on Kubernetes"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon deployment using Kubernetes."
tags:
    - setup
    - kubernetes
    - install
---

If you are here, it means that you have a Kubernetes cluster and [helm](/guides/setup-helm/) setup.

Please consider reading our [configuration guides](/configuration/introduction/) to have a deeper knowledge about how to configure and customize Polyaxon to your need,
we also made this [interactive app](https://install.polyaxon.com) to help you navigate the most important options to install Polyaxon.

Please also check the [helm reference](/references/polyaxon-helm-reference/) for all default values.

## Create a namespace for Polyaxon

Polyaxon is installed and relies on the namespace to run experiments
independently of other applications running on your cluster, we recommend using `polyaxon`.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

If you would like to use a different name, you must keep im mind to update the `namespace` value in your config.

## Configuration

This section will guide you through how you can create a configuration file to deploy Polyaxon.
Polyaxon ships with [default values](/references/polyaxon-helm-reference/), however and depending on your use case
you might need to [override](/configuration/introduction/) some of these values.
To do so, you need to create a configuration file and we recommend to save it somewhere safe so that you can reuse it in the future.

Create a config file `config.yaml` or `polyaxon_config.yaml`,
and set up all information you want to override in the default config.

Example, disabling ingress and RBAC

```yaml
rbac:
  enabled: false

ingress:
  enabled: false

serviceType: LoadBalancer
```

Example, adding database persistence

```yaml
postgresql:
  persistence:
    enabled: true
    size: 5Gi
```

Example, updating the default user:

```yaml
user:
  username: "root"
  email: "root@polyaxon.local"
  password: "dummypassword"
```

## Install Polyaxon

First of all, you need to [add](https://github.com/kubernetes/helm/blob/master/docs/chart_repository.md) the [Polyaxon helm repository](https://charts.polyaxon.com/)
to your helm, so you can install Polyaxon from it.
This makes it easy to refer to the Polyaxon chart without having to use a long URL each time.


```bash
$ helm repo add polyaxon https://charts.polyaxon.com
$ helm repo update
```

Now you can install Polyaxon with your `config.yml` file

```bash
$ helm install polyaxon/polyaxon \
    --name=<RELEASE_NAME> \
    --namespace=<NAMESPACE> \
    -f config.yml
```

`--name` is an identifier used by helm to refer to this deployment.
You need it when you are changing the configuration of this install or deleting it.
We recommend using `RELEASE_NAME = polyaxon` or `RELEASE_NAME = plx`.

`--namespace` should be the same value of the namespace you created in the first step,
we again recommend using `polyaxon` to make it always easy to remember.

> TIP: We recommend using `polyaxon` for both the `--name` and `--namespace` to avoid too much confusion.
    The same command with `polyaxon` as a value:

    ```bash
    $ helm install polyaxon/polyaxon \
    --name=polyaxon \
    --namespace=polyaxon \
    -f config.yml
    ```

>NOTE: "Release name already exists error"
> If you get a release named `<RELEASE_NAME>` already exists error, then you should delete the release by running `helm delete --purge <RELEASE_NAME>`.

You can see the pods being created by entering in a different terminal:

```bash
$ kubectl --namespace=<NAMESPACE> get pod
```

When helm is done deploying Polyaxon, it will output some instructions `NOTES`,
these note will be different depending on your configuration (the service type used and / or ingress);

```
NOTES:
Polyaxon is currently running:


1. Get the application URL by running these commands:

     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status by running:
           'kubectl get --namespace polyaxon svc -w polyaxon-polyaxon-api'


  export POLYAXON_IP=$(kubectl get svc --namespace polyaxon polyaxon-polyaxon-ingress -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

  export POLYAXON_HTTP_PORT=80
  export POLYAXON_WS_PORT=80

  echo http://$POLYAXON_IP:$POLYAXON_HTTP_PORT

2. Setup your cli by running theses commands:

  polyaxon config set --host=$POLYAXON_IP --http_port=$POLYAXON_HTTP_PORT  --ws_port=$POLYAXON_WS_PORT


3. Log in with superuser

  USER: root
  PASSWORD: Get login password with

    kubectl get secret --namespace polyaxon polyaxon-polyaxon-secret -o jsonpath="{.data.POLYAXON_ADMIN_PASSWORD}" | base64 --decode
```

These notes are important for setting the CLI, and getting access to the dashboard.

Next step you need the [Polyaxon CLI installed](/setup/cli/), and you need to configure 
the host and the ports based on these notes.


## Install Polyaxon On Minikube

For [Minikube](https://github.com/kubernetes/minikube), we recommend Virtualbox/VMware drivers, but you can also use other drivers.

We recommend also to increase the amount of resources allocates:

```bash
minikube start --cpus 4 --memory 8192 --disk-size=40g
```

By default Minikube allocates 2Gb of RAM, this not enough for Polyaxon and we recommend at least 6Gb.

By default Polyaxon uses ingress (with serviceType ClusterIP) and RBAC, you might need to disable one / both of them in your `config.yml`/`polyaxon_config.yml`:

```yaml
isMinikube: true

rbac:
  enabled: false

ingress:
  enabled: false

serviceType: LoadBalancer
```

It is however recommended to enable RBAC and start minikube with the option `--extra-config=apiserver.authorization-mode=RBAC`.

After installing polyaxon, you might need to use the following command to enable access to the API service:

```bash
minikube service -n polyaxon polyaxon-polyaxon-api
```

Note that when using minikube, the IP address of the application is given by `minikube ip`.

## Upgrade Polyaxon

To upgrade Polyaxon to a newer version, you can simply run:

```bash
helm update
helm upgrade polyaxon polyaxon/polyaxon -f polyaxon-config.yml
```

## Applying configuration changes

The general method to modify your Kubernetes deployment is to:

 1. Make a change to the config.yml
 2. Run a helm upgrade:

    ```bash
    $ helm upgrade <RELEASE_NAME> polyaxon/polyaxon -f config.yml
    ```

    Where `<RELEASE_NAME>` is the parameter you passed to `--name` when installing polyaxon with `helm install`.

    If you don’t remember it, you can probably find it by doing `helm list`.

    If you used the default values suggested in the docs, the `<RELEASE_NAME>` should be `polyaxon`

  3. Wait for the upgrade to finish, and make sure that when you do
  `kubectl --namespace=<NAMESPACE> get pod` the pods are in Ready state.

    Your configuration change has been applied!


## Turn off Polyaxon

When you are done with Polyaxon, you can turn off the deployment,
and depending on your persistence configuration you can keep all your data saved for future deployments.

You can also decide to completely turn off Polyaxon and remove the namespace and computational resources.

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
