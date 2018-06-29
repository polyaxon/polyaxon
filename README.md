# Polyaxon-chart

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Release](https://img.shields.io/badge/release-0.1.0-green.svg?longCache=true)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)

Helm charts for creating reproducible and maintainable deployments of Polyaxon with Kubernetes.

## TL;DR;

```console
$ helm install polyaxon --name polyaxon --namespace polyaxon
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

This chart can be installed on single node or multi-nodes cluster,
in which case you need to provide some volumes with `ReadWriteMany`.
An nfs provisioner can be enabled in cases where you want to try the platform on multi-nodes cluster
without the need to create your own volumes.

> **Warning**: You should know that using the nfs provisioner is not meant to be a production option.

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
$ helm install --name=<RELEASE_NAME> --wait polyaxon/polyaxon
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
| `namespace`                     | The namespace that will be used by Polyaxon to create experiments and communicate with other services| `polyaxon`

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
| `persistence.logs.mountPath`      | Path where to mount the volume                    | `/logs`
| `persistence.logs.hostPath`       | The directory from the host node's                | `/tmp/logs`


**repos**: code used for creating builds, training experiments, running jobs.

If you don't provide an outputs claim to use, Polyaxon will use the host.

| Parameter                         | Description                                       | Default
| --------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.logs.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.logs.mountPath`      | Path where to mount the volume                    | `/repos`
| `persistence.logs.hostPath`       | The directory from the host node's                | `/tmp/repos`


**upload**: temporary volume where Polyaxon uploads data, code, files, ...

If you don't provide an outputs claim to use, Polyaxon will use the host.
It is not very important to have a volume claim for this, if your host node has sufficient storage.

| Parameter                         | Description                                       | Default
| --------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.logs.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.logs.mountPath`      | Path where to mount the volume                    | `/repos`
| `persistence.logs.hostPath`       | The directory from the host node's                | `/tmp/repos`


**data**: data used for training experiments.

You can mount multiple claims and host paths for data.
This should be a dictionary mapping volume names to the respective volumes.

Every definition should follow the following structure:


| Parameter                                  | Description                                       | Default
| ------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.data.dataName.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.data.dataName.mountPath`      | Path where to mount the volume                    | ``
| `persistence.data.dataName.hostPath`       | The directory from the host node's                | ``
| `persistence.data.dataName.readOnly`       | Whether to mount as read only                     |


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
```


**outputs**: outputs generated from experiments and jobs.

You can mount multiple claims and host paths for outputs.
This should be a dictionary mapping volume names to the respective volumes.

Every definition should follow the following structure:


| Parameter                                        | Description                                       | Default
| ------------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------
| `persistence.outputs.outputsName.existingClaim`  | Name of an existing PVC                           | ``
| `persistence.outputs.outputsName.mountPath`      | Path where to mount the volume                    | ``
| `persistence.outputs.outputsName.hostPath`       | The directory from the host node's                | ``
| `persistence.outputs.outputsName.readOnly`       | Whether to mount as read only                     |


The default value based is on a path in the host node:

```yaml
persistence:
  outputs:
    default-outputs:
      mountPath: "/outputs"
      hostPath: "/outputs"
```

Example of different outputs persistence definition:

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
```

### Persistence with nfs provisioner

Polyaxon provides options to enable a built-in nfs provisioner to create some of the persistence storage needed or all of them.
In order to use this provisioner, you need disable the persistence option, and optional adjust the provisioner size for that volume.

```yaml
nfsProvisioner:
  enabled: true
  persistence:
    enabled: true
```

**logs**:

To use the provisioner for the logs, you should disable `persistence.logs`

```yaml
persistence:
  logs: null
```

And to adjust the behavior of the provisioner for the logs, for example the size:

```yaml
nfsProvisioner:
  enabled: true
  persistence:
    enabled: true
  pvc:
    logs:
      size: 10Gi
```

| Parameter                                | Description                                       | Default
| ---------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `nfsProvisioner.pvc.logs.name`           | Name of the PVC to create                         | `polyaxon-pvc-logs`
| `nfsProvisioner.pvc.logs.size`           | Size of data volume                               | `5Gi`
| `nfsProvisioner.pvc.logs.mountPath`      | Path to mount the volume at, to use other image   | `/logs`
| `nfsProvisioner.pvc.logs.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


**repos**:

To use the provisioner for the repos, you should disable `persistence.repos`

```yaml
persistence:
  repos: null
```

And to adjust the behavior of the provisioner for the repos, for example the size:

```yaml
nfsProvisioner:
  enabled: true
  persistence:
    enabled: true
  pvc:
    repos:
      size: 50Gi
```

| Parameter                                 | Description                                       | Default
| ----------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `nfsProvisioner.pvc.repos.name`           | Name of the PVC to create                         | `polyaxon-pvc-repos`
| `nfsProvisioner.pvc.repos.size`           | Size of data volume                               | `10Gi`
| `nfsProvisioner.pvc.repos.mountPath`      | Path to mount the volume at, to use other image   | `/repos`
| `nfsProvisioner.pvc.repos.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


**upload**:

To use the provisioner for the upload, you should disable `persistence.upload`

```yaml
persistence:
  upload: null
```

And to adjust the behavior of the provisioner for the upload, for example the size:

```yaml
nfsProvisioner:
  enabled: true
  persistence:
    enabled: true
  pvc:
    upload:
      size: 50Gi
```

| Parameter                                  | Description                                       | Default
| ------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------
| `nfsProvisioner.pvc.upload.name`           | Name of the PVC to create                         | `polyaxon-pvc-upload`
| `nfsProvisioner.pvc.upload.size`           | Size of data volume                               | `50Gi`
| `nfsProvisioner.pvc.upload.mountPath`      | Path to mount the volume at, to use other image   | `/upload`
| `nfsProvisioner.pvc.upload.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


**data**:

To use the provisioner for the data as well, you should disable `persistence.data`

```yaml
persistence:
  data: null
```

And to adjust the behavior of the provisioner for the data, for example the size:

```yaml
nfsProvisioner:
  enabled: true
  persistence:
    enabled: true
  pvc:
    data:
      size: 50Gi
```

| Parameter                                | Description                                       | Default
| ---------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `nfsProvisioner.pvc.data.name`           | Name of the PVC to create                         | `polyaxon-pvc-data`
| `nfsProvisioner.pvc.data.size`           | Size of data volume                               | `10Gi`
| `nfsProvisioner.pvc.data.mountPath`      | Path to mount the volume at, to use other image   | `/data`
| `nfsProvisioner.pvc.data.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


**outputs**:

To use the provisioner for the outputs as well, you should disable `persistence.outputs`

```yaml
persistence:
  outputs: null
```

And to adjust the behavior of the provisioner for the outputs, for example the size:

```yaml
nfsProvisioner:
  enabled: true
  persistence:
    enabled: true
  pvc:
    outputs:
      size: 50Gi
```

| Parameter                                   | Description                                       | Default
| ------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------
| `nfsProvisioner.pvc.outputs.name`           | Name of the PVC to create                         | `polyaxon-pvc-outputs`
| `nfsProvisioner.pvc.outputs.size`           | Size of data volume                               | `10Gi`
| `nfsProvisioner.pvc.outputs.mountPath`      | Path to mount the volume at, to use other image   | `/outputs`
| `nfsProvisioner.pvc.outputs.accessMode`     | Use volume as ReadOnly or ReadWrite ReadWriteOnce | `ReadWriteMany`


### Node and Deployment manipulation

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `nodeSelector.core`                | Node labels for pod assignment for core                      | `{}`
| `nodeSelector.experiments`         | Node labels for pod assignment for experiments               | `{}`
| `nodeSelector.jobs`                | Node labels for pod assignment for core                      | `{}`
| `nodeSelector.builds`              | Node labels for pod assignment for experiments               | `{}`
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
