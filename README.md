# Polyaxon-chart

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

Helm charts for creating reproducible and maintainable deployments of Polyxaon with Kubernetes.

## TL;DR;

```console
$ helm install --wait polyaxon
```

## Introduction

This chart bootstraps a [Polyaxon](polyaxon.com) deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

It also packages some required for Polyaxon.:
 * [PostgreSQL](https://github.com/kubernetes/charts/tree/master/stable/postgresql)
 * [Redis](https://github.com/kubernetes/charts/tree/master/stable/redis)
 * [Rabbitmq](https://github.com/kubernetes/charts/tree/master/stable/rabbitmq)
 * [Docker-Registry](https://github.com/kubernetes/charts/tree/master/incubator/docker-registry)

> **Warning**: This chart does not yet allow for you to specify your own database host, redis host, rabbitmq host.

## Prerequisites

- Kubernetes >= 1.7.0 
- helm >= v2.5.0

## Installing the Chart

To install the chart with the release name `my-release`:

```console
$ helm install --name my-release --wait stable/polyaxon
```

If you encounter an error, please use the `--wait` flag

```console
$ helm install --name my-release --wait stable/polyaxon
```

> **Note**: We have to use the --wait flag for initial creation because the database creationg takes longer than the default 300 seconds

The command deploys Polyaxon on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```console
$ helm delete my-release
```

or with `--purge` flag

```console
$ helm delete my-release --purge
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following tables lists the configurable parameters of the Sentry chart and their default values.

| Parameter               | Description                                                                    | Default                                                    |
| ------------------------| -------------------------------------------------------------------------------| ---------------------------------------------------------- |
| `useRBAC`               | Use Kubernetes' role-based access control (RBAC)                               | `true`                                                     |
| `nodeSelectors`         | To schedule Polyaxon Core components on specific labeled nodes in Kubernetes.  | `empty`                                                     |
| `imagePullPolicy`       | Image pull policy                                                              | `IfNotPresent`                                             |

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
