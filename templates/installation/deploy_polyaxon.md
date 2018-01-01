If you are here, it means that you have a Kubernetes cluster and helm setup,
if not please read how you can [install kubernetes](install_kubernetes), and [setup helm](setup_helm).

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

Since you are going to use this configuration file in the future, we recommend to save it somewhere safe.

Create a config file `config.yml` or `polyaxon_config.yml`,
and set up all information you want to override in the default config.

e.g.

```yaml
polyaxonSecret: "RANDOM_STRING"

user:
  username: "root"
  email: "root@polyaxon.local"
  password: "root"
```

## Install Polyaxon

First of all, you need to add the [Polyaxon helm repository](https://github.com/kubernetes/helm/blob/master/docs/chart_repository.md)
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
    --namespace=<NAMESPAC> \
    -f config.yaml
```

`--name` is an identifier used by helm to refer to this deployment.
You need it when you are changing the configuration of this install or deleting it.
We recommend using `RELEASE_NAME = polyaxon` or `RELEASE_NAME = plx`.

`--namespace` should be the same value of the name space you created in the first step,
we again recommend using `polyaxon` to make it always easy to remember.

!!! Tip
    We recommend using `polyaxon` for both the `--name` and `--namespace` to avoid too much confusion.
    The same command with `polyaxon` as a value:

    ```bash
    $ helm install polyaxon/polyaxon \
    --name=polyaxon \
    --namespace=polyaxon \
    -f config.yaml
    ```

??? note "Release name already exists error"
    If you get a release named `<RELEASE_NAME>` already exists error,
    then you should delete the release by running `helm delete --purge <RELEASE_NAME>`.

You can see the pods being created by entering in a different terminal:

```bash
$ kubectl --namespace=<NAMESPACE> get pod
```

When helm is done deploying Polyaxon it will output some instructions `NOTES`

```
```

These notes are important for setting the CLI, and getting access to the dashboard.

Next step we will [install the CLI](install_polyaxon_cli) and configure the host and the ports based on the these notes.

You can also check how you can [extend this deployment](/customization/extend_deployments)
in [many ways](/reference_polyaxon_helm).
