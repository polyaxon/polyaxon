---
title: "Artifacts Connections"
sub_link: "connections/artifacts"
meta_title: "Connections for your dataset, artifacts, volumes and storage in Polyaxon - Configuration"
meta_description: "Polyaxon allows to use volumes as well as cloud stores for storing outputs and artifacts, and connecting datasets."
tags:
  - configuration
  - polyaxon
  - kubernetes
  - docker-compose
  - environment
  - orchestration
  - volumes
  - aws
  - gcp
  - azure
sidebar: "setup"
---

You can connect as many datasets, volumes, and artifacts stores in Polyaxon.

It's better to set a connection for each dataset, or artifacts store, or volume path holding some data,
to get more visibility and granular control over who is using that connection and how often.

Exposing each dataset or artifacts as a connection also gives you the possibility to
effectively version your data, and expose information about the changes from one dataset version to another in the description.
By using connections you can also migrate and find jobs that use a dataset, and take necessary actions.

Using multiple connections is also very useful for large teams who need either to scale or
to have different teams access different volumes and storage backends.

This section tries to explain how Polyaxon mounts these volumes for experiments and jobs.

## Default behavior

When no connection is provided, the default behavior is to use a local path on the host node for storing outputs and logs.
Oftentimes this default behavior is sufficient for users who are just trying the platform, and don't want to deal with configuration steps.

## Host paths


### Schema Fields

You can use host paths to define storage connections:

  * hostPath: the host path.
  * mountPath: path where to mount the volume content in the container
  * readOnly: if the volume should be mounted in read-only mode.

> **Note**: If you the node where the host path is defined is lost, all data will be lost as well.

### Example usage as the default artifactsStore

```yaml
artifactsStore:
  name: my-artifacts-store
  kind: host_path
  schema:
    mountPath: "/artifacts"
    hostPath: "/path/to/artifacts"
```

### Example usage in connections

```yaml
connections:
  ...
  - name: my-artifacts-store
    kind: host_path
    schema:
      mountPath: "/artifacts"
      hostPath: "/path/to/artifacts"
```

## Persistent Volumes

You can use a [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to store your outputs and artifacts, or to connect datasets:

### Schema Fields

  * volumeClaim: volume claim name.
  * mountPath: path where to mount the volume content in the container
  * readOnly: if the volume should be mounted in read-only mode.

### Example usage as the default artifactsStore

```yaml
artifactsStore:
  name: my-volume
  kind: volume_claim
  schema:
    mountPath: "/tmp/outputs"
    volumeClaim: "outputs-2-pvc"
```

### Example usage in connections

```yaml
connections:
  ...
  - name: my-volume
    kind: volume_claim
    schema:
      mountPath: "/datasets/path"
      volumeClaim: "dataset-2-pvc"
```

If you are using a persistent volume with one node access you need to be aware that you can only use it with experiment/jobs running on that same node at the same time.

There are some options that support multi-nodes access, e.g. a PVC backed with an [NFS](/integrations/artifacts-on-nfs/)/Glusterfs server,
where you can use multiple nodes and schedule experiments on all the nodes to access the artifacts/datasets.
Please refer to [this section](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) to learn more about access modes.

## Cloud stores

In order to mount a cloud storage,
you need to provide authentication access to Polyaxon for the storage needed during the scheduling.

The way to do that is by creating a secret of your cloud storage access,
and providing the secret name.

> **Tip**: You can use the same k8s secret to configure multiple connections.

### Schema Fields

  * bucket: the bucket you want to expose in this connection.


### Example usage as the default artifactsStore

```yaml
artifactsStore:
  name: azure-bucket
  kind: wasb
  schema: {"bucket": "wasbs://bucket@owner.blob.core.windows.net/"}
  secret:
    name: "az-secret"
```

### Example usage in connections

```yaml
connections:
  ...
  - name: azure-bucket
    kind: wasb
    schema: {"bucket": "wasbs://bucket@owner.blob.core.windows.net/"}
    secret:
      name: "az-secret"
  - name: s3-bucket
    kind: s3
    schema: {"bucket": "s3://bucket/"}
    secret:
      name: "s3-secret"
  - name: gcs-bucket2
    kind: gcs
    schema: {"bucket": "gs://bucket/"}
    secret:
      name: "gcs-secret"
```

## Integrations guides

Please refer to this integration sections for more details on how to use:

 * [artifactsStore](/integrations/artifacts/) with different providers and backends to manage artifacts, logs, and outputs.
 * [connections](/integrations/data-stores/) with different providers and backends to mount datasets.
