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
Polyaxon ships with [default values](/reference_polyaxon_helm), however and depending on your use case
you might need to override some of these values.
To do so, you need to create a configuration file and we recommend to save it somewhere safe so that you can reuse it in the future.

Create a config file `config.yml` or `polyaxon_config.yml`,
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

Example, updating the user data:

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

!!! Tip
    We recommend using `polyaxon` for both the `--name` and `--namespace` to avoid too much confusion.
    The same command with `polyaxon` as a value:

    ```bash
    $ helm install polyaxon/polyaxon \
    --name=polyaxon \
    --namespace=polyaxon \
    -f config.yml
    ```

??? note "Release name already exists error"
    If you get a release named `<RELEASE_NAME>` already exists error,
    then you should delete the release by running `helm delete --purge <RELEASE_NAME>`.

You can see the pods being created by entering in a different terminal:

```bash
$ kubectl --namespace=<NAMESPACE> get pod
```

When helm is done deploying Polyaxon, it will output some instructions `NOTES`,
that depends on the service type used and / or ingress;

```
NOTES:
Polyaxon is currently running:


1. Get the application URL by running these commands:

     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch the status by running:
           'kubectl get --namespace polyaxon svc -w polyaxon-polyaxon-api'


  export POLYAXON_IP=$(kubectl get svc --namespace polyaxon polyaxon-polyaxon-api -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

  export POLYAXON_HTTP_PORT=80

  export POLYAXON_WS_PORT=1337

  echo http://$POLYAXON_IP:$POLYAXON_HTTP_PORT

2. Setup your cli by running theses commands:

  polyaxon config set --host=$POLYAXON_IP --http-port=$POLYAXON_HTTP_PORT  --ws-port=$POLYAXON_WS_PORT


3. Log in with superuser

  USER: root
  PASSWORD: Get login password with

    kubectl get secret --namespace polyaxon polyaxon-polyaxon-secret -o jsonpath="{.data.user-password}" | base64 --decode
```

These notes are important for setting the CLI, and getting access to the dashboard.

Next step we will [install the CLI](install_polyaxon_cli) and configure the host and the ports based on the these notes.

You can also check how you can [extend this deployment](/customization/extend_deployments)
in [many ways](/reference_polyaxon_helm).


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

