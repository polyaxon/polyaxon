---
title: "Polyaxon Helm Reference"
sub_link: "polyaxon-helm-reference"
meta_title: "Polyaxon Helm Reference - Polyaxon References"
meta_description: "Polyaxon chart is a Helm chart for creating reproducible and maintainable deployments of Polyaxon with Kubernetes."
visibility: public
status: published
tags:
  - specification
  - polyaxon
  - yaml
  - helm
  - reference
  - kubernetes
---

Polyaxon chart is a Helm chart for creating reproducible and maintainable deployments of Polyaxon with Kubernetes.

## Introduction

This chart bootstraps a [Polyaxon](https://polyaxon.com) deployment on
a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

It also packages some required dependencies for Polyaxon:

 * [PostgreSQL](https://github.com/bitnami/charts/tree/main/bitnami/postgresql)
 * [Redis](https://github.com/bitnami/charts/tree/main/bitnami/redis)
 * [Rabbitmq](https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq)

> **Note**: It's possible to provide your own managed version of each one for these dependencies.

This chart can be installed on a single node or multi-nodes cluster,
in which case you need to provide some volumes with `ReadWriteMany` or cloud buckets.
An nfs provisioner can be used in cases where you want to try the platform on a multi-nodes cluster
without the need to create your own volumes. Please see [polyaxon-nfs-provisioner](https://github.com/polyaxon/polyaxon-nfs-provisioner)

> **Tip**: The full list of the default [values.yaml](https://github.com/polyaxon/polyaxon-chart/blob/master/polyaxon/values.yaml)

## Prerequisites

- Kubernetes >= 1.5.0
- helm >= v2.5.0


## Add polyaxon charts

```bash
helm repo add polyaxon https://charts.polyaxon.com
helm repo update
```

## Installing the Chart

To install the chart with the release name `<RELEASE_NAME>`:

```bash
helm install --name=<RELEASE_NAME> --namespace=<NAMESPACE> polyaxon/polyaxon
```

Please do not use the `--wait` flag, otherwise the deployment will not succeed.

The command deploys Polyaxon on the Kubernetes cluster in the default configuration.

The [configuration](#configuration) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`


## Uninstalling the Chart

To uninstall/delete the `<RELEASE_NAME>` deployment:

```bash
helm delete <RELEASE_NAME>
```

or with `--purge` flag

```bash
helm delete <RELEASE_NAME> --purge
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

> **Warning**:
> Jobs are only deleted if they succeeded,
> sometimes if you cancel a deployment you might end up with undeleted jobs.

```bash
kubectl delete job ...
```

> **Note**: You can delete the chart and skip the cleaning the hooks

```bash
helm del --purge  <RELEASE_NAME>  --no-hooks
```

This can be particularly useful if your deployment is not working, because the hooks will most probably fail.

### How to set the configuration

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example:

```bash
helm install --name=<RELEASE_NAME> \
    --namespace=<NAMESPACE>\
    --set persistence.enabled=false,email.host=email \
    polyaxon
```

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example:

```bash
helm install --name my-release -f values.yaml polyaxon
```

## DeploymentType

| Parameter                       | Description                                                                                                           | Default
| --------------------------------| ----------------------------------------------------------------------------------------------------------------------| ----------------------------------------------------------
| `DeploymentType`                | The deployment type tells polyaxon how to show instructions ('kubernetes', 'minikube', 'microk8s', 'docker-compose')  | `kubernetes`


## deploymentVersion

| Parameter                       | Description                                                                                                                                             | Default
| --------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------
| `deploymentVersion`             | The deployment version to use, this is important if you are using polyaxon-cli to avoid accidentally deploying/upgrading to a version without noticing  | `latest`


## Namespace

| Parameter                       | Description                                                                                          | Default
| --------------------------------| -----------------------------------------------------------------------------------------------------| ----------------------------------------------------------
| `namespace`                     | The namespace that will be used by Polyaxon to create operations and communicate with other services| `polyaxon`

## Ingress, RBAC, and API service

This chart provides support for an Ingress resource with a custom ingress controller `polyaxon-ingress`.
You can also provide different annotations for the ingress and it will not use `polyaxon-ingress` class. (`ingress.annotations.kubernetes.io/ingress.class`)

| Parameter                | Description                                        | Default
| ------------------------ | -------------------------------------------------- | ----------------------------------------------------------
| `rbac.enabled`           | Use Kubernetes role-based access control (RBAC)    | `true`
| `ingress.enabled`        | Use Kubernetes ingress                             | `true`
| `ingress.path`           | Kubernetes ingress path                            | `/`
| `ingress.hostName`       | Kubernetes ingress hostName                        | ``
| `ingress.annotations`    | Ingress annotations                                | `{}`
| `ingress.tls`            | Use Ingress TLS                                    | `[]`
| `api.service.annotations`| API Service annotations                            | `{}`


Note: using TLS requires either:
 - a preconfigured secret with the TLS secrets in it
 - or the user of [cert-manager](https://github.com/bitnami/charts/tree/main/bitnami/cert-manager) to auto request certs from let's encrypt and store them in a secret.

It's also possible to use a service like [externalDNS](https://github.com/bitnami/charts/tree/main/bitnami/external-dns) to auto create the DNS entry for the polyaxon API service.

## Securing API server with TLS

If you have your own certificate you can make a new secret with the `tls.crt` and the `tls.key`,
then set the secret name in the values file.

### Automating TLS certificate creation and DNS setup

To automate the creation and registration of new domain name you can use the following services:

* [cert-manager](https://github.com/bitnami/charts/tree/main/bitnami/cert-manager)
* [externalDNS](https://github.com/bitnami/charts/tree/main/bitnami/external-dns) (Route53 / Google CloudDNS)

once installed, you can set the values for `ingress.tls`:

```yaml
ingress:
  enabled: true
  hostName: polyaxon.acme.com
  tls:
    - secretName: polyaxon.acme-tls
      hosts:
        - polyaxon.acme.com
```

TLS can have more than one host.

In order to get the domain registration to work you need to set the value of `api.service.annotations`
to the annotation needed for your domain:
i.e

```yaml
annotations:
  domainName: polyaxon.my.domain.com
```

## SSL

| Parameter | Description                                                             | Default
| ----------| ------------------------------------------------------------------------| ----------------------------------------------------------
| `ssl`     | To set ssl and serve https with Polyaxon deployed with NodePort service | `{}`


NGINX acts as a reverse proxy for Polyaxon's front-end server, meaning NGINX proxies external HTTP (and HTTPS) requests to the Polyaxon API.

### NGINX ingress

The recommended way to use Https in Polyaxon on Kubernetes is by setting an ingress-nginx for the Polyaxon Cluster running on Kubernetes.

Polyaxon's helm chart comes with an ingress resource that you can use with an ingress controller where you should use TLS so that all traffic will be served over HTTPS.

 1. Create a TLS secret that contains your TLS certificate and private key.

    ```bash
    kubectl create secret tls polyaxon-tls --key $PATH_TO_KEY --cert $PATH_TO_CERT
    ```


 2. Add the tls configuration to Polyaxon's Ingress values. (**Do not use CluserIP on GKE**)

    ```yaml
    serviceType: ClusterIP
    ingress:
      enabled: true
      hostName: polyaxon.acme.com
      tls:
      - secretName: polyaxon.acme-tls
        hosts:
          - polyaxon.acme.com
    ```

    For more information visit the [Nginx Ingress Integration](/integrations/nginx/)

### NGINX for NodePort service

To enable ssl for Polyaxon API running with NodePort service on Kubernetes, you need to provide an ssl certificate and SSL certificate key.

you can provide a self-signed certificate or a browser trusted certificate.

 1. Create a secret for your certificate:

    ```bash
    kubectl create -n polyaxon secret generic polyaxon-cert --from-file=/path/to/certs/polyaxon.com.crt --from-file=/path/to/certs/polyaxon.com.key
    ```

 2. Make sure to update your deployment config with reference to the certificate

    ```yaml
    ssl:
      enabled: true
      secretName: 'polyaxon-cert'
    ```
 3. Set the service type to `NodePort` and update the API's service port to 443.

 N.B. By default, Polyaxon mounts the ssl certificate and key to `/etc/ssl`, this value can be updated using the `.Values.ssl.path`.

## CLI setup

If you are serving Polyaxon on HTTPS, you should be aware that CLI need to have a different config:

```bash
polyaxon config set --host=IP/Host [--verify_ssl]
```


## dns

| Parameter | Description                                                             | Default
| ----------| ------------------------------------------------------------------------| ----------------------------------------------------------
| `dns`     | DNS configuration for cluster running with custom dns setup             | `{}`


Several users deploy Polyaxon on Kubernetes cluster created with [kubespray](https://github.com/kubernetes-sigs/kubespray),
and by default Kubespray creates Kubernetes with CoreDNS as a cluster DNS server.

### Update DNS backend

Although we could provide logic to detect the DNS used in the cluster, this would require cluster wide RBAC that we think it's unnecessary.
The default DNS backend used by Polyaxon is KubeDNS, to set it to a different DNS, you can provide this value in your Polyaxon's deployment config:

```yaml
dns:
  backend: "coredns"
```

### Update DNS prefix to different system

Since the DNS service is generally deployed on `kube-system` namespace, the default DNS prefix is `kube-dns.kube-system` or `coredns.kube-system` if you update the previous option.

You can also provide the complete DNS prefix, and not use the DNS backend options:

```yaml
dns:
  prefix: "kube-dns.other-kube-system"
```

### Update the DNS prefix for OpenShift

OpenShift has a different DNS configuration, the default prefix is:

```yaml
dns:
  prefix: "dns-default.openshift-dns"
```

### Update DNS cluster

The default dns cluster used in Polyaxon to resolve routes is `cluster.local`, you can provide a Custom Cluster DNS, by setting:

```yaml
dns:
  customCluster: "custom.cluster.name"
```


### Time zone

To set a different time zone for application (convenient for the dashboard and admin interface)
you can can provide a [valid time zone value](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)


| Parameter | Description         | Default
| ----------| --------------------| ----------------------------------------------------------
| `timezone`| The timezone to use | `UTC`


### Root user

The default superuser/root user for polyaxon.
A default password is provided, `rootpassword`.
You can also remove the value and Polyaxon will generate a random password that you can retrieve later.

| Parameter                       | Description                                 | Default
| --------------------------------| --------------------------------------------| ----------------------------------------------------------
| `user.username`                 | Default superuser username                  | `root`
| `user.email`                    | Default superuser email                     | `root@polyaxon.local`
| `user.password`                 | Default superuser password (could be null)  | `rootpassword`


### Nvidia GPU

In order to use GPU for your experiments you need to have nodes with GPU and you need to expose the NVidia paths to your jobs.

This is how you specify where your NVidia library is on your host

| Parameter             | Description                                                           | Default
| ----------------------| ----------------------------------------------------------------------| ----------------------------------------------------------
| `dirs.nvidia.lib`     | The nvidia lib:e .g "/usr/lib/nvidia-384"                             | ``
| `dirs.nvidia.bin`     | The nvidia bin:e .g "/usr/lib/nvidia-384/bin"                         | ``
| `dirs.nvidia.libcuda` | The nvidia libcuda.so.1:e .g "/usr/lib/x86_64-linux-gnu/libcuda.so.1" | ``

This where you want to mount these libraries on the pods, by default Polyaxon will same values from dirs if not provided.

| Parameter                   | Description                                                           | Default
| ----------------------------| ----------------------------------------------------------------------| ----------------------------------------------------------
| `mountPaths.nvidia.lib`     | The nvidia lib:e .g "/usr/lib/nvidia-384"                             | `dirs.nvidia.lib`
| `mountPaths.nvidia.bin`     | The nvidia bin:e .g "/usr/lib/nvidia-384/bin"                         | `dirs.nvidia.bin`
| `mountPaths.nvidia.libcuda` | The nvidia libcuda.so.1:e .g "/usr/lib/x86_64-linux-gnu/libcuda.so.1" | `dirs.nvidia.libcuda`

### Persistence

Polyaxon provides options to enable or disable persistence, or connect existing claims.
You can set the options for setting up the persistence for Polyaxon,
or enable the nfs provisioner to provision the volumes, or some of them.

> **Tip**: If you are using a multi node cluster and need to have `ReadWriteMany` volumes for trying out the platform,
> you can use the nfs provisioner provided by the platform. See later [Persistence with nfs](#persistence-with-nfs-provisioner)

For `logs` and `repos` Polyaxon by default uses the host node, in many cases this is a sufficient default,
in other cases where Polyaxon is deployed on a multi-nodes and is replicated,
the usage of `ReadWriteMany` PVC is recommended to have a stable deployment.

**logs**: logs generated by experiments/jobs/builds.

If you don't provide an outputs claim to use, Polyaxon will use the host.

| Parameter                         | Description                                       | Default
| --------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.logs.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.logs.mountPath`      | Path where to mount the volume                    | `/polyaxon-logs`
| `persistence.logs.hostPath`       | The directory from the host node's                | `/tmp/logs`


**repos**: code used for creating builds, training experiments, running jobs.

If you don't provide an outputs claim to use, Polyaxon will use the host.

| Parameter                         | Description                                       | Default
| --------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.repos.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.repos.mountPath`      | Path where to mount the volume                    | `/polyaxon-repos`
| `persistence.repos.hostPath`       | The directory from the host node's                | `/tmp/repos`


**upload**: temporary volume where Polyaxon uploads data, code, files, ...

If you don't provide an outputs claim to use, Polyaxon will use the host.
It is not very important to have a volume claim for this if your host node has sufficient storage.

| Parameter                         | Description                                       | Default
| --------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.upload.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.upload.mountPath`      | Path where to mount the volume                    | `/polyaxon-upload`
| `persistence.upload.hostPath`       | The directory from the host node's                | `/tmp/upload`


**data**: data used for training experiments.

You can mount multiple claims and host paths for data.
This should be a dictionary mapping volume names to the respective volumes.

Every definition should follow the structure:


| Parameter                                  | Description                                       | Default
| ------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.data.dataName.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.data.dataName.mountPath`      | Path where to mount the volume                    | ``
| `persistence.data.dataName.hostPath`       | The directory from the host node's                | ``
| `persistence.data.dataName.readOnly`       | Whether to mount as read-only                     |
| `persistence.data.dataName.store`          | To mount a cloud storage (s3, gcs, azure)         |
| `persistence.data.dataName.bucket`         | The bucket to mount                               |
| `persistence.data.dataName.secret`         | The secret containing access to the bucket        |
| `persistence.data.dataName.secretKey`      | The key name to get the value from the secret     |


The default value based is on a path in the host node:

```yaml
persistence:
  data:
    default-data:
      mountPath: "/data"
      hostPath: "/data"
```

Example of different data persistence definition:

```yaml
persistence:
  data:
    data1:
      mountPath: "/data/1"
      hostPath: "/path/to/data"
      readOnly: true
    data2:
      mountPath: "/data/2"
      existingClaim: "data-2-pvc"
    data-foo:
      mountPath: "/data/foo"
      existingClaim: "data-foo-pvc"
    data-gcs3:
      store: gcs
      bucket: gs://data-bucket
      secret: secret-name
      secretKey: secret-key
    data-s3:
      store: s3
      bucket: s3://data-bucket
      secret: secret-name
      secretKey: secret-key
    data-azure:
      store: azure
      bucket: wasbs://data-container@account.blob.core.windows.net/
      secret: secret-name
      secretKey: secret-key
```


**outputs**: outputs generated from experiments and jobs.

You can mount multiple claims and host paths for outputs.
This should be a dictionary mapping volume names to the respective volumes.

Every definition should follow the structure:


| Parameter                                        | Description                                       | Default
| ------------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.outputs.outputsName.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.outputs.outputsName.mountPath`      | Path where to mount the volume                    | ``
| `persistence.outputs.outputsName.hostPath`       | The directory from the host node's                | ``
| `persistence.outputs.outputsName.readOnly`       | Whether to mount as read-only                     |
| `persistence.outputs.dataName.store`             | To mount a cloud storage (s3, gcs, azure)         |
| `persistence.outputs.dataName.bucket`            | The bucket to mount                               |
| `persistence.outputs.dataName.secret`            | The secret containing access to the bucket        |
| `persistence.outputs.dataName.secretKey`         | The key name to get the value from the secret     |


The default value based is on a path in the host node:

```yaml
persistence:
  outputs:
    default-outputs:
      mountPath: "/outputs"
      hostPath: "/outputs"
```

> N.B. Multi-outputs is not supported in CE version

Example of multi-outputs persistence definition with:

```yaml
persistence:
  outputs:
    outputs1:
      mountPath: "/outputs/1"
      hostPath: "/path/to/outputs"
      readOnly: true
    outputs2:
      mountPath: "/outputs/2"
      existingClaim: "outputs-2-pvc"
    outputs-foo:
      mountPath: "/outputs/foo"
      existingClaim: "outputs-foo-pvc"
    outputs-gcs3:
      store: gcs
      bucket: gs://outputs-bucket
      secret: secret-name
      secretKey: secret-key
    outputs-s3:
      store: s3
      bucket: s3://outputs-bucket
      secret: secret-name
      secretKey: secret-key
    outputs-azure:
      store: azure
      bucket: wasbs://outputs-container@account.blob.core.windows.net/
      secret: secret-name
      secretKey: secret-key
```

### Node and Deployment manipulation

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `nodeSelector`                     | Node selector for core pod assignment                        | `{}`
| `tolerations`                      | Tolerations for core pod assignment                          | `[]`
| `affinity`                         | Affinity for core                                            | Please check the values


Dependent charts can also have values overwritten. Preface values with

 * `postgresql.*`
 * `redis.*`
 * `rabbitmq.*`


Polyaxon provides a list of options to select which nodes should be used for the core platform, for the dependencies, and for the runs.


### Node Selectors

Polyaxon comes with a couple of node selectors options to assign pods to nodes for polyaxon's core platform

Additionally every dependency in the helm package, exposes a node selector option.

By providing these values, or some of them,
you can constrain the pods belonging to that category to only run on
particular nodes or to prefer to run on particular nodes.

```yaml
nodeSelector:
  ...

postgresql:
  nodeSelector:
    ...

redis:
  master:
    nodeSelector:
      ...
  slave:
    nodeSelector:
      ...

rabbitmq:
  nodeSelector:
    ...
```

### Tolerations

If one or more taints are applied to a node,
and you want to make sure some pods should not deploy on it,
Polyaxon provides tolerations option for the core platform, as well as for all dependencies, e.i. database, broker, expose their own tolerations option.

```yaml
tolerations:
  ...

postgresql:
  tolerations:
    ...

redis:
  master:
    tolerations:
      ...
  slave:
    tolerations:
      ...

rabbitmq:
  tolerations:
    ...
```

### Affinity

It allows you to constrain which nodes your pod is eligible to schedule on, based on the node's labels.
Polyaxon has a default `Affinity` values for its core components to ensure that they deploy on the same node.

Polyaxon's default affinity:

```yaml
affinity:
  podAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: type
              operator: In
              values:
              - "polyaxon-core"
          topologyKey: "kubernetes.io/hostname"
```

You can update your config deployment file to set affinity for each dependency:


```yaml
affinity:
  ...

postgresql:
  affinity:
    ...

redis:
  master:
    affinity:
      ...
  slave:
    affinity:
      ...

rabbitmq:
  affinity:
    ...
```

### Resources discovery

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `resourcesDaemon.enabled`          | resourcesDaemon enabled                                      | `true`
| `resourcesDaemon.tolerations`      | Tolerations for resourcesDaemon pod assignment               | `[]`


### IPs/Hosts White list

In order to restrict IP addresses and hosts that can communicate with the API

```yaml
allowedHosts:
  - 127.0.0.1
  - 159.203.150.212
  - .mysite.com  # (Will consume every subdomain of mysite.com)
```

### API Host

In order to receive email and notifcation with a clickable link to the objects on the platform

```yaml
hostName: 159.203.150.212
```
Or

```yaml
hostName: polyaxon.foo.com
```

### Admin view

Polyaxon ships with an admin interface:


```yaml
ui:
 adminEnabled: true
```

## Security context

| Parameter                               | Description                                                                                         | Default
| --------------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------
| `enabled`                               | enable security context                                                                             | `false`
| `runAsUser`                             | security context UID                                                                                | `2222`
| `runAsGroup`                            | security context GID                                                                                | `2222`
| `fsGroup`                               | security context FS                                                                                 | `2222`
| `allowPrivilegeEscalation`              | Controls whether a process can gain more privileges than its parent process                         | `false`
| `runAsNonRoot`                          | Indicates that the container must run as a non-root user                                            | `true`
| `fsGroupChangePolicy`                   | defines behavior of changing ownership and permission of the volume before being exposed inside Pod |

Polyaxon runs all containers as root by default, this configuration is often fine for several deployment,
however, in some use cases it can expose a compliance issue for some teams.

Polyaxon provides a simple way to enable a security context for all core components.

Default configuration:

```yaml
securityContext:
  enabled: false
  runAsUser: 2222
  runAsGroup: 2222
  fsGroup: 2222
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  fsGroupChangePolicy:
```

### Enable security context

```yaml
securityContext:
  enabled: true
```

Or enable with custom UID/GID other than 2222/2222:

```yaml
securityContext:
  enabled: true
  user: 1111
  group: 1111
```

Define behavior of changing ownership and permission of the volume before being exposed inside Pod:

```yaml
securityContext:
  enabled: true
  fsGroupChangePolicy: OnRootMismatch
```

This will enable a security context to run all containers using a UID/GID == 1111/1111.

> **N.B.** If you are using a host path or a volume for the artifacts store, make sure to allow the UID/GID to access it.

## Port forwarding

You can use port forwarding to access the API and dashboard on localhost:

```bash
kubectl port-forward  svc/polyaxon-polyaxon-api 31811:80 31812:1337 -n polyaxon
```

## Upgrade Polyaxon

To upgrade Polyaxon to a newer version, you can simply run:
```bash
helm repo update
helm upgrade polyaxon polyaxon/polyaxon -f config.yaml
```
