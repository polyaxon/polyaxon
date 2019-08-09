# Polyaxon-chart

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.org/polyaxon/polyaxon-chart.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-chart)
[![Release](https://img.shields.io/badge/release-0.5.5-green.svg?longCache=true)](https://github.com/polyaxon/polyaxon/releases/tag/0.5.5)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)

Polyaxon chart is a Helm chart for creating reproducible and maintainable deployments of Polyaxon with Kubernetes.

## TL;DR;

```bash
$ helm install polyaxon --name polyaxon --namespace polyaxon
```

Or if you are using Polyaxon-CLI

```bash
$ polyaxon deploy
```

## Introduction

This chart bootstraps a [Polyaxon](https://polyaxon.com) deployment on
a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

It also packages some required dependencies for Polyaxon:

 * [PostgreSQL](https://github.com/kubernetes/charts/tree/master/stable/postgresql)
 * [Redis](https://github.com/kubernetes/charts/tree/master/stable/redis)
 * [Rabbitmq](https://github.com/kubernetes/charts/tree/master/stable/rabbitmq-ha)
 * [Docker-Registry](https://github.com/helm/charts/tree/master/stable/docker-registry)


> **Note**: It's possible to provide your own managed version of each one fo these dependecies.

This chart can be installed on single node or multi-nodes cluster,
in which case you need to provide some volumes with `ReadWriteMany` or cloud buckets.
An nfs provisioner can be used in cases where you want to try the platform on multi-nodes cluster
without the need to create your own volumes. Please see [polyaxon-nfs-provisioner](https://github.com/polyaxon/polyaxon-nfs-provisioner)

> **Tip**: The full list of the default [values.yaml](https://github.com/polyaxon/polyaxon-chart/blob/master/polyaxon/values.yaml)


## Prerequisites

- Kubernetes >= 1.5.0
- helm >= v2.5.0


## Add polyaxon charts

```bash
$ helm repo add polyaxon https://charts.polyaxon.com
$ helm repo update
```

## Installing the Chart

To install the chart with the release name `<RELEASE_NAME>`:

```bash
$ helm install --name=<RELEASE_NAME> --namespace=<NAMESPACE> --wait polyaxon/polyaxon
```

If you encounter an error, please use the `--wait` flag

```bash
$ helm install --name=<RELEASE_NAME> --wait polyaxon/polyaxon
```

The command deploys Polyaxon on the Kubernetes cluster in the default configuration.

The [configuration](#configuration) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`


## Uninstalling the Chart

To uninstall/delete the `<RELEASE_NAME>` deployment:

```bash
$ helm delete <RELEASE_NAME>
```

or with `--purge` flag

```bash
$ helm delete <RELEASE_NAME> --purge
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

> **Warning**:
Jobs are only deleted if they succeeded,
sometimes if you cancel a deployment you might end up with undeleted jobs.

```bash
$ kubectl delete job ...
```

> **Note**:
You can delete the chart and skip the cleaning the hooks

```bash
helm del --purge  <RELEASE_NAME>  --no-hooks
```

This can be particularly useful if your deployment is not working, because the hooks will most probably fail.

### How to set the configuration

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example:

```bash
$ helm install --name=<RELEASE_NAME> \
    --namespace=<NAMESPACE>\
    --set persistence.enabled=false,email.host=email \
    polyaxon
```

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example:

```bash
$ helm install --name my-release -f values.yaml polyaxon
```

### DeploymentType

| Parameter                       | Description                                                                                                           | Default
| --------------------------------| ----------------------------------------------------------------------------------------------------------------------| ----------------------------------------------------------
| `DeploymentType`                | The deployment type tells polyaxon how to show instructions ('kubernetes', 'minikube', 'microk8s', 'docker-compose')  | `kubernetes`


### deploymentVersion

| Parameter                       | Description                                                                                                                                             | Default
| --------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------
| `deploymentVersion`             | The deployment version to use, this is important if you are using polyaxon-cli to avoid accidentally deploying/upgrading to a version without noticing  | `latest`


### Namespace

| Parameter                       | Description                                                                                          | Default
| --------------------------------| -----------------------------------------------------------------------------------------------------| ----------------------------------------------------------
| `namespace`                     | The namespace that will be used by Polyaxon to create experiments and communicate with other services| `polyaxon`

### Ingress, RBAC, and API service

This chart provides support for Ingress resource with a custom ingress controller `polyaxon-ingress`.
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
 - or the user of [cert-manager](https://github.com/helm/charts/tree/master/stable/cert-manager) to auto request certs from let's encrypt and store them in a secret.

It's also possible to use a service like [externalDNS](https://github.com/helm/charts/tree/master/stable/external-dns) to auto create the DNS entry for the polyaxon API service.

### Securing api server with TLS

If you have your own certificate you can make a new secret with the `tls.crt` and the `tls.key`,
then set the secret name in the values file.

#### Automating TLS certificate creation and DNS setup

To automate the creation and registration of new domain name you can use the following services:

* [cert-manager](https://github.com/helm/charts/tree/master/stable/cert-manager)
* [externalDNS](https://github.com/helm/charts/tree/master/stable/external-dns) (Route53 / Google CloudDNS)

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

### SSL

| Parameter | Description                                                             | Default
| ----------| ------------------------------------------------------------------------| ----------------------------------------------------------
| `ssl`     | To set ssl and serve https with Polyaxon deployed with NodePort service | `{}`

### dns

| Parameter | Description                                                             | Default
| ----------| ------------------------------------------------------------------------| ----------------------------------------------------------
| `dns`     | DNS configuration for cluster running with custom dns setup             | `{}`

### Time zone

To set a different time zone for application (convenient for the dashboard and admin interface)
you can can provide a [valid time zone value](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)


| Parameter | Description         | Default
| ----------| --------------------| ----------------------------------------------------------
| `timeZone`| The timezone to use | `UTC`


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
you can use the nfs provisioner provided by the platform. See later [Persistence with nfs](#persistence-with-nfs-provisioner)

For `logs` and `repos` Polyaxon by default uses the host node, in many case this is a sufficient default,
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
It is not very important to have a volume claim for this, if your host node has sufficient storage.

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
| `persistence.data.dataName.readOnly`       | Whether to mount as read only                     |
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
| `persistence.outputs.outputsName.readOnly`       | Whether to mount as read only                     |
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
 * `rabbitmq-ha.*`
 * `docker-registry.*`


### Resources discovery

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `resourcesDaemon.enabled`          | resourcesDaemon enabled                                      | `true` 
| `resourcesDaemon.tolerations`      | Tolerations for resourcesDaemon pod assignment               | `[]` 


### IPs/Hosts White list

In order to restrict IP addresses and hosts that can communicate with the api

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

Polyaxon ships with an admin interface, it is disabled by default.


```yaml
adminViewEnabled: true
```

## Port forwarding

You can use port forwarding to access the api and dashboard on localhost:

```bash
kubectl port-forward  svc/polyaxon-polyaxon-api 31811:80 31812:1337 -n polyaxon
```

## Upgrade Polyaxon

To upgrade Polyaxon to a newer version, you can simply run:
```bash
helm repo update
helm upgrade polyaxon polyaxon/polyaxon -f polyaxon-config.yml
```


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-chart.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-chart?ref=badge_large)
