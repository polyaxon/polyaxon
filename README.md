# Polyaxon-chart

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

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
sometime if you can cancel a deployment you might end up with undeleted jobs.

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

| Parameter                       | Description                                      | Default
| --------------------------------| -------------------------------------------------| ----------------------------------------------------------
| `rbac.enabled`                  | Use Kubernetes' role-based access control (RBAC) | `true`
| `ingress.enabled`               | Use Kubernetes' ingress                          | `true`
| `ingress.annotations`           | Ingress annotations                              | `{}`


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

In order to use GPU for you experiment you need to have nodes with GPU and you need to expose the NVidia paths to you dockers.

This is how you specify where you NVidia library is on you host

| Parameter             | Description                                                           | Default
| ----------------------| ----------------------------------------------------------------------| ----------------------------------------------------------
| `dirs.nvidia.lib`     | The nvidia lib:e .g "/usr/lib/nvidia-384"                             | ``
| `dirs.nvidia.bin`     | The nvidia bin:e .g "/usr/lib/nvidia-384/bin"                         | ``
| `dirs.nvidia.libcuda` | The nvidia libcuda.so.1:e .g "/usr/lib/x86_64-linux-gnu/libcuda.so.1" | ``

This where you want to mount these libraries on the pods

| Parameter                   | Description                                                           | Default
| ----------------------------| ----------------------------------------------------------------------| ----------------------------------------------------------
| `mountPaths.nvidia.lib`     | The nvidia lib:e .g "/usr/lib/nvidia-384"                             | ``
| `mountPaths.nvidia.bin`     | The nvidia bin:e .g "/usr/lib/nvidia-384/bin"                         | ``
| `mountPaths.nvidia.libcuda` | The nvidia libcuda.so.1:e .g "/usr/lib/x86_64-linux-gnu/libcuda.so.1" | ``

### Persistence

Polyaxon provides options to enable or disable persistence, or connect existing claims for


**data**: data used for training experiments.

If you don't provide a data claim to use, Polyaxon will use the host.

| Parameter                        | Description                                     | Default
| ---------------------------------| ------------------------------------------------| ----------------------------------------------------------
| `persistence.data.existingClaim` | Name of an existing PVC                         | ``
| `persistence.data.size`          | Size of data volume                             | `10Gi`
| `persistence.data.mountPath`     | Path to mount the volume at, to use other image | `/data`
| `persistence.data.subPath`       | Subpath to mount the volume at.                 | ``
| `persistence.data.accessMode`    | Use ReadWriteOnce or ReadWriteMany              | `ReadWriteMany`

**outputs**: outputs generated form experiments.

If you don't provide a outputs claim to use, Polyaxon will use the host.

| Parameter                           | Description                                     | Default
| ------------------------------------| ------------------------------------------------| ----------------------------------------------------------
| `persistence.outputs.existingClaim` | Name of an existing PVC                         | ``
| `persistence.outputs.size`          | Size of data volume                             | `5Gi`
| `persistence.outputs.mountPath`     | Path to mount the volume at, to use other image | `/outputs`
| `persistence.outputs.subPath`       | Subpath to mount the volume at.                 | ``
| `persistence.outputs.accessMode`    | Use volume as ReadWriteOnce or ReadWriteMany    | `ReadWriteMany`


**repos**: code used to for training your experiments.

If you no persistence is used Polyaxon will use an empty dir `{}`.

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


**logs**: logs generated by experiments.

If you no persistence is used Polyaxon will use an empty dir `{}`.

| Parameter                         | Description                                      | Default
| ----------------------------------| -------------------------------------------------| ----------------------------------------------------------
| `persistence.logs.enabled`       | use persistence for logs                          | `false`
| `persistence.logs.name`          | Name of the PVC                                   | `polyaxon-pvc-repos`
| `persistence.logs.storageClass`  | Storage class of backing PVC                      | ``
| `persistence.logs.existingClaim` | Name of an existing PVC                           | ``
| `persistence.logs.size`          | Size of data volume                               | `5Gi`
| `persistence.logs.mountPath`     | Path to mount the volume at, to use other image   | `/repos`
| `persistence.logs.subPath`       | Subpath to mount the volume at.                   | ``
| `persistence.logs.accessMode`    | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteOnce`

**uploads**: temporary volume where Polyaxon uploaded data, code, files, ...

If you no persistence is used Polyaxon will use an empty dir `{}`.

| Parameter                           | Description                                       | Default
| ------------------------------------| --------------------------------------------------| ----------------------------------------------------------
| `persistence.uploads.enabled`       | use persistence for uploads                       | `false`
| `persistence.uploads.name`          | Name of the PVC                                   | `polyaxon-pvc-repos`
| `persistence.uploads.storageClass`  | Storage class of backing PVC                      | ``
| `persistence.uploads.existingClaim` | Name of an existing PVC                           | ``
| `persistence.uploads.size`          | Size of data volume                               | `5Gi`
| `persistence.uploads.mountPath`     | Path to mount the volume at, to use other image   | `/repos`
| `persistence.uploads.subPath`       | Subpath to mount the volume at.                   | ``
| `persistence.uploads.accessMode`    | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteOnce`


### Node and Deployment manipulation

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `nodeSelector.core`                | Node labels for pod assignment for core                      | `{}`
| `nodeSelector.experiments`         | Node labels for pod assignment for experiments               | `{}`
| `tolerations.core`                 | Toleration labels for pod assignment for core                | `[]`
| `tolerations.resourcesDaemon`      | Toleration labels for pod assignment for resourcesDaemon     | `[]`
| `affinity`                         | Path to mount the volume at, to use other image              | Please check the values


Dependent charts can also have values overwritten. Preface values with
 * `postgresql.*`
 * `redis.*`
 * `rabbitmq.*`
 * `registry.*`


Dependent charts can also have values overwritten. Preface values with `postgresql.*`, `redis.*`, `rabbitmq.*`, or `registry.*`

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
