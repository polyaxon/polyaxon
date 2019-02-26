---
title: "Customize logs storage"
sub_link: "custom-logs-storage"
meta_title: "Customize Logs Volumes and Storage in Polyaxon - Configuration"
meta_description: "Polyaxon allows to use volumes as well as cloud storages for storing logs."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
    - environment
    - orchestration
    - volumes
    - s3
    - gcp
    - azure-storage
sidebar: "configuration"
---

Polyaxon allows to mount a volume or a cloud storage to store logs.

## Default behaviour

When the user does not provide any logs configuration, the default behaviour is to use a local path on the host node for storing logs, 
this behaviour allows Polyaxon deployment to finish successfully cases without raising any errors.

Often times this default value is sufficient for users who are just trying the platform, and don't want to deal with configuration steps.

> N.B. for the community version you can only use one logs backend storage.

## Chart Definition

The [helm reference](/references/polyaxon-helm-reference/#persistence) describes briefly the logs persistence definitions,
and how you can mount volumes, both persistent claims, host paths, and cloud storages:


```yaml
persistence:
  logs:
    ...
```

For a multi-nodes deployment we recommend using `ReadWriteMany` persistent volume or one a cloud storages, such as S3 or GCS.

## Host paths

You can use host paths to define a logs storage:

```yaml
persistence:
  logs:
    mountPath: "/polyaxon-logs"
    hostPath: "/path/to/logs"
```

Users must know when to use host paths, we do not recommend this option for a multi-nodes deployment, 
because several Polyaxon components might not be able to access the logs to function correctly if they are scheduled on different nodes.

Users should be aware as well, that by losing the node where the host path is defined, all logs will be lost as well.

## Persistent Volumes

You can use a [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to store your logs:

```yaml
persistence:
  logs:
    mountPath: "/polyaxon-logs"
    existingClaim: "logs-pvc"
```

If you are using a persistent volume with one node access you need to be aware that some Polyaxon components must be scheduled on the same node.

Users must know when to use a single access volume, we do not recommend this option for a multi-nodes deployment where the API, scheduler, are replicated over multiple nodes, 
because several Polyaxon components might not be able to access the logs to function correctly if they are scheduled on different nodes.

There are some options that support multi-nodes access, e.g. a PVC backed with an [NFS](/integrations/logs-on-nfs/)/Glusterfs server, 
where you can use multiple nodes, this allows you to easily scale your API, scheduler and have access to read and write logs. 
Please refer to [this section](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) to learn more about access modes.

## Cloud storages

In order to mount a cloud storage, 
users need to provide authentication access to Polyaxon for the storage needed during the scheduling.

The way to do that is by creating a secret of your cloud storage access auth, 
and providing the secret name and key name to use from that secret. 
(You can use the same k8s secret to manage multiple storage access auth, in this case only the key will be different).

Please refer to this integration sections for more details:

 * [Logs on GCS](/integrations/logs-on-gcs/)
 * [Logs on AWS S3](/integrations/logs-on-s3/)
 * [Logs on Azure storage](/integrations/logs-on-azure/)
