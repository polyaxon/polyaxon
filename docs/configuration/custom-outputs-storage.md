---
title: "Customize outputs storage"
sub_link: "custom-outputs-storage"
meta_title: "Customize Outputs Volumes and Storage in Polyaxon - Configuration"
meta_description: "Polyaxon allows to use volumes as well as cloud storages for storing outputs and artifacts."
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

Polyaxon allows to mount a volume or a cloud storage to store outputs.

## Default behaviour

When the user does not provide any outputs configuration, the default behaviour is to use a local path on the host node for storing outputs, 
this behaviour allows Polyaxon deployment to finish successfully cases without raising any errors.

Often times this default value is sufficient for users who are just trying the platform, and don't want to deal with configuration steps.

> N.B. for the community version you can only use one outputs backend storage.

## Chart Definition

The [helm reference](/references/polyaxon-helm-reference/#persistence) describes briefly the outputs persistence definitions,
and how you can mount volumes, both persistent claims, host paths, and cloud storages:


```yaml
persistence:
  outputs:
    outputs:
      ...
```

For a multi-nodes deployment we recommend using `ReadWriteMany` persistent volume or one a cloud storages, such as S3 or GCS.

## Host paths

You can use host paths to define an outputs storage:

```yaml
persistence:
  outputs:
    outputs:
      mountPath: "/outputs/1"
      hostPath: "/path/to/outputs"
```

Users must know when to use host paths, we do not recommend this option for a multi-nodes deployment, 
because different jobs/experiments might be scheduled on a different node and store their artifacts on different nodes. 
Several Polyaxon components might not be able to access the outputs to display or give option to download artifacts for a certain job/experiment.

Users should be aware as well, that by losing the node where the host path is defined, all outputs will be lost as well.

## Persistent Volumes

You can use a [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to store your outputs and artifacts:

```yaml
persistence:
  outputs:
    outputs:
      mountPath: "/polyaxon-outputs"
      existingClaim: "outputs-pvc"
```

If you are using a persistent volume with one node access you need to be aware that you can only use it with experiment/jobs running on that same node at the same time.

We do not recommend this option for a multi-nodes deployment, 
because different jobs/experiments might be scheduled on a different node and store their artifacts on different nodes. 
Several Polyaxon components might not be able to access the outputs to display or give option to download artifacts for a certain job/experiment.

There are some options that support multi-nodes access, e.g. a PVC backed with an [NFS](/integrations/outputs-on-nfs/)/Glusterfs server, 
where you can use multiple nodes and schedule experiments on all the nodes to access the outputs. Please refer to [this section](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) to learn more about access modes.

## Cloud storages

In order to mount a cloud storage, 
users need to provide authentication access to Polyaxon for the storage needed during the scheduling.

The way to do that is by creating a secret of your cloud storage access auth, 
and providing the secret name and key name to use from that secret. 
(You can use the same k8s secret to manage multiple storage access auth, in this case only the key will be different).

Please refer to this integration sections for more details:

 * [Outputs on GCS](/integrations/outputs-on-gcs/)
 * [Outputs on AWS S3](/integrations/outputs-on-s3/)
 * [Outputs on Azure storage](/integrations/outputs-on-azure/)
