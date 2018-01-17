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

It also packages some required for Polyaxon.:

 * [PostgreSQL](https://github.com/kubernetes/charts/tree/master/stable/postgresql)
 * [Redis](https://github.com/kubernetes/charts/tree/master/stable/redis)
 * [Rabbitmq](https://github.com/kubernetes/charts/tree/master/stable/rabbitmq)
 * [Docker-Registry](https://github.com/kubernetes/charts/tree/master/incubator/docker-registry)

> **Warning**: This chart does not yet allow for you to specify your own database host, redis host, rabbitmq host.

## Prerequisites

- Kubernetes >= 1.8.0
- helm >= v2.5.0

## Installing the Chart

To install the chart with the release name `<RELEASE_NAME>`:

```console
$ helm install --name=<RELEASE_NAME> --namespace=<NAMESPACE> --wait stable/polyaxon
```

If you encounter an error, please use the `--wait` flag

```console
$ helm install --name=<RELEASE_NAME> --wait stable/polyaxon
```

The command deploys Polyaxon on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

!!! tip
    List all releases using `helm list`


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

** __warning__ **
Jobs are only deleted if they succeeded,
sometime if you can cancel a deployment you might end up with undeleted jobs.

```console
$ kubectl delete job ...
```

## Configuration

The following tables lists the configurable parameters of the Polyaxon chart and their default values.

| Parameter                       | Description                                                                    | Default
| --------------------------------| -------------------------------------------------------------------------------| ----------------------------------------------------------
| `rbac.enabled`                  | Use Kubernetes' role-based access control (RBAC)                               | `true`
| `ingress.enabled`               | Use Kubernetes' ingress                                                        | `true`
| `user.username`                 | Default superuser's username.                                                  | `root`
| `user.email`                    | Default superuser's email.                                                     | `root@local.com`
| `user.password`                 | Default superuser's password.                                                  | `root`
| `dirs.nvidia.bin`               | nvidia path for GPU (bin)                                                      | ``
| `dirs.nvidia.lib`               | nvidia path for GPU (lib)                                                      | ``
| `dirs.nvidia.libcuda`           | nvidia path for GPU (libcuda)                                                  | ``
| `persistence.output.enabled`    | use persistence for output                                                     | `true`
| `persistence.logs.enabled`      | use persistence for logs                                                       | `false`
| `persistence.repos.enabled`     | use persistence for repos                                                      | `false`
| `persistence.uploads.enabled`   | use persistence for uploads                                                    | `false`

Dependent charts can also have values overwritten. Preface values with `postgresql.*`, `redis.*`, `rabbitmq.*`, or `registry.*`

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```console
$ helm install --name my-release \
  --set persistence.enabled=false,email.host=email \
    polyaxon
```

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example,

```console
$ helm install --name my-release -f values.yaml polyaxon
```

> **Tip**: You can use the default [values.yaml](polyaxon/values.yaml)

## Ingress

This chart provides support for Ingress resource with an ingress controller.
You can also provide different annotations for the ingress and it will not use `polyaxon-ingress` class.
