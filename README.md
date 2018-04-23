# Polyaxon-chart

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Release](https://img.shields.io/badge/release-0.0.7-green.svg?longCache=true)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)

Helm charts for creating reproducible and maintainable deployments of Polyaxon with Kubernetes.

## TL;DR;

```console
$ helm install --wait polyaxon
```

## Introduction

This chart bootstraps a [Polyaxon](https://polyaxon.com) deployment on
a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

It also packages some required dependencies for Polyaxon:

 * [PostgreSQL](https://github.com/kubernetes/charts/tree/master/stable/postgresql)
 * [Redis](https://github.com/kubernetes/charts/tree/master/stable/redis)
 * [Rabbitmq](https://github.com/kubernetes/charts/tree/master/stable/rabbitmq)
 * [Docker-Registry](https://github.com/kubernetes/charts/tree/master/incubator/docker-registry)

> **Warning**: This chart does not yet allow for you to specify your own database host, redis host, rabbitmq host.

## Prerequisites

- Kubernetes >= 1.8.0
- helm >= v2.5.0


## Add polyaxon charts

```console
$ helm repo add polyaxon https://charts.polyaxon.com
$ helm repo update
```

## Installing the Chart

To install the chart with the release name `<RELEASE_NAME>`:

```console
$ helm install --name=<RELEASE_NAME> --namespace=<NAMESPACE> --wait polyaxon/polyaxon
```

If you encounter an error, please use the `--wait` flag

```console
$ helm install --name=<RELEASE_NAME> --wait stable/polyaxon
```

The command deploys Polyaxon on the Kubernetes cluster in the default configuration.

The [configuration](#configuration) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`


## Uninstalling the Chart

To uninstall/delete the `<RELEASE_NAME>` deployment:

```console
$ helm delete <RELEASE_NAME>
```

or with `--purge` flag

```console
$ helm delete <RELEASE_NAME> --purge
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

> **Warning**:
Jobs are only deleted if they succeeded,
sometime if you cancel a deployment you might end up with undeleted jobs.

```console
$ kubectl delete job ...
```


## Configuration

The following tables lists the configurable parameters of the Polyaxon chart and their default values.

### Namespace

| Parameter                       | Description                                                                                          | Default
| --------------------------------| -----------------------------------------------------------------------------------------------------| ----------------------------------------------------------
| `namespace`                  | The namespace that will be used by Polyaxon to create experiments and communicate with other services| `polyaxon`

### Ingress, RBAC, and API service

This chart provides support for Ingress resource with a custom ingress controller `polyaxon-ingress`.
You can also provide different annotations for the ingress and it will not use `polyaxon-ingress` class. (`ingress.annotations.kubernetes.io/ingress.class`)

| Parameter            | Description                                      | Default
| ---------------------| -------------------------------------------------| ----------------------------------------------------------
| `rbac.enabled`       | Use Kubernetes' role-based access control (RBAC) | `true`
| `ingress.enabled`    | Use Kubernetes' ingress                          | `true`
| `ingress.annotations`| Ingress annotations                              | `{}`


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
| `user.emailFrom`                | Default superuser email from                | `<root@polyaxon.local>`
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


**data**: data used for training experiments.

If you don't provide a data claim to use, Polyaxon will use the host.

| Parameter                        | Description                                     | Default
| ---------------------------------| ------------------------------------------------| ----------------------------------------------------------
| `persistence.data.existingClaim` | Name of an existing PVC                         | ``
| `persistence.data.size`          | Size of data volume                             | `10Gi`
| `persistence.data.mountPath`     | Path to mount the volume at, to use other image | `/data`
| `persistence.data.subPath`       | Subpath to mount the volume at.                 | ``
| `persistence.data.accessMode`    | Use ReadWriteOnce or ReadWriteMany              | `ReadWriteMany`

**outputs**: outputs generated from the experiments.

If you don't provide an outputs claim to use, Polyaxon will use the host.

| Parameter                           | Description                                     | Default
| ------------------------------------| ------------------------------------------------| ----------------------------------------------------------
| `persistence.outputs.existingClaim` | Name of an existing PVC                         | ``
| `persistence.outputs.size`          | Size of data volume                             | `5Gi`
| `persistence.outputs.mountPath`     | Path to mount the volume at, to use other image | `/outputs`
| `persistence.outputs.subPath`       | Subpath to mount the volume at.                 | ``
| `persistence.outputs.accessMode`    | Use volume as ReadWriteOnce or ReadWriteMany    | `ReadWriteMany`


**logs**: logs generated by experiments.

If you don't provide an outputs claim to use, Polyaxon will use the host.

| Parameter                         | Description                                      | Default
| ----------------------------------| -------------------------------------------------| ----------------------------------------------------------
| `persistence.logs.existingClaim` | Name of an existing PVC                           | ``
| `persistence.logs.size`          | Size of data volume                               | `5Gi`
| `persistence.logs.mountPath`     | Path to mount the volume at, to use other image   | `/logs`
| `persistence.logs.subPath`       | Subpath to mount the volume at.                   | ``
| `persistence.logs.accessMode`    | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


**repos**: code used for training your experiments.

If no persistence is used Polyaxon will use an empty dir `{}`.

| Parameter                         | Description                                       | Default
| ----------------------------------| --------------------------------------------------| ----------------------------------------------------------
| `persistence.repos.enabled`       | use persistence for repos                         | `false`
| `persistence.repos.name`          | Name of the PVC                                   | `polyaxon-pvc-repos`
| `persistence.repos.storageClass`  | Storage class of backing PVC                      | ``
| `persistence.repos.existingClaim` | Name of an existing PVC                           | ``
| `persistence.repos.size`          | Size of data volume                               | `5Gi`
| `persistence.repos.mountPath`     | Path to mount the volume at, to use other image   | `/repos`
| `persistence.repos.subPath`       | Subpath to mount the volume at.                   | ``
| `persistence.repos.accessMode`    | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteOnce`


**upload**: temporary volume where Polyaxon uploads data, code, files, ...

If no persistence is used Polyaxon will use an empty dir `{}`.

| Parameter                           | Description                                       | Default
| ------------------------------------| --------------------------------------------------| ----------------------------------------------------------
| `persistence.upload.enabled`        | use persistence for upload                        | `false`
| `persistence.upload.name`           | Name of the PVC                                   | `polyaxon-pvc-upload`
| `persistence.upload.storageClass`   | Storage class of backing PVC                      | ``
| `persistence.upload.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.upload.size`           | Size of data volume                               | `5Gi`
| `persistence.upload.mountPath`      | Path to mount the volume at, to use other image   | `/repos`
| `persistence.upload.subPath`        | Subpath to mount the volume at.                   | ``
| `persistence.upload.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteOnce`


### Node and Deployment manipulation

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `nodeSelector.core`                | Node labels for pod assignment for core                      | `{}`
| `nodeSelector.experiments`         | Node labels for pod assignment for experiments               | `{}`
| `tolerations.core`                 | Toleration labels for pod assignment for core                | `[]`
| `tolerations.resourcesDaemon`      | Toleration labels for pod assignment for resourcesDaemon     | `[]`
| `affinity`                         | Affinity for core                                            | Please check the values


Dependent charts can also have values overwritten. Preface values with

 * `postgresql.*`
 * `redis.*`
 * `rabbitmq.*`
 * `registry.*`


### How to set the configuration

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```console
$ helm install --name=<RELEASE_NAME> \
    --namespace=<NAMESPACE>\
    --set persistence.enabled=false,email.host=email \
    polyaxon
```

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example,

```console
$ helm install --name my-release -f values.yaml polyaxon
```

> **Tip**: You can use the default [values.yaml](polyaxon/values.yaml)


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-chart.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-chart?ref=badge_large)
