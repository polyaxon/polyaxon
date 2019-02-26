---
title: "Customize Data storage"
sub_link: "custom-data-storage"
meta_title: "Customize Data Volumes and Storage in Polyaxon - Configuration"
meta_description: "Polyaxon allows to mount multiple data volumes as well as cloud storages."
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

Polyaxon allows to mount multiple data volumes as well as cloud storages,
this could be very useful for large teams who need either to scale or
to have different teams to access different volumes.

This section tries to explain how Polyaxon mounts these volumes for experiments and jobs.

## Default behaviour

When the user does not provide any data configuration, the default behaviour is to use a local path on the host node for data, 
this behaviour allows Polyaxon deployment to finish successfully cases without raising any errors.

Often times this default value is sufficient for users who are just trying the platform, and don't want to deal with configuration steps.


## Chart Definition

The [helm reference](/references/polyaxon-helm-reference/#persistence) describes briefly the data persistence definitions,
and how you can mount volumes, both persistent claims, host paths, and cloud storages, here's the example coming from the ref:

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

For GCS, S3, and Azure Storage, you need to need to provide a secret with auth access to these storages.

## Scheduling

When the user defines a multi data volumes,
Polyaxon has a default behavior for mounting these volumes during the scheduling of the jobs and experiments,
unless the user overrides this default behavior in the polyaxonfiles.

If the polyaxonfile for running an experiment or a job does not define the data volume or volumes that it needs access to,
Polyaxon will by default mount all these volumes when it schedules the experiment or the job.

These data volumes will be accessible to you as a dictionary `{volume_name: path_to_data}`,
exported as an env variable `POLYAXON_RUN_DATA_PATHS`.

You can use as well our `tracking` api in `polyaxon-client` to get access to this [env variable automatically](/references/polyaxon-tracking-api/paths/#get-data-paths).

If on the other hand, you wish to only mount one volume or a subset of the volumes,
you then need to provide this information in the polyaxonfile, e.g.

```yaml
environment:
  persistence:
    data: ['data1', 'data-foo']
```

By providing this persistence subsection,
Polyaxon will only mount these volumes by looking up there names from the defined volumes.

## Host paths

You can use host paths to define a data storage:

```yaml
persistence:
  data:
    data-path1:
      mountPath: "/data/1"
      hostPath: "/path/to/data"
    data-path2:
      mountPath: "/data/2"
      hostPath: "/path/to/data"
      readOnly: true
```

In the example above we defined 2 host paths with one with path read only permission.

Users must know when to use host paths, especially in a multi-nodes deployment, 
because jobs/experiments might only find an empty path if scheduled on a different node that the one where the data resides.

You can look at how you can customize the node scheduling behaviour in this [guide](/configuration/custom-node-scheduling/).

## Persistent Volumes

You can use multiple [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to store your data and use them in Polyaxon:

```yaml
persistence:
  data:
    data-pvc1:
      mountPath: "/data-pvc/1"
      existingClaim: "data-pvc-1"
    data-pvc2:
      mountPath: "/data-pvc/2"
      existingClaim: "data-pvc-2"
```

If you are using a persistent volume with one node access you need to be aware that you can only use it with experiment/jobs running on that node at the same time.

There are some options that support multi-nodes access, e.g. a PVC backed with an [NFS](/integrations/data-on-nfs/)/Glusterfs server, 
where you can use multiple nodes and schedule experiments on all the nodes to access the data. Please refer to [this section](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) to learn more about access modes.

## Cloud storages

In order to mount a cloud storage, 
users need to provide authentication access to Polyaxon for all storages needed during the scheduling.

The way to do that is by creating a secret of your cloud storage access auth, 
and providing the secret name and key name to use from that secret. 
(You can use the same k8s secret to manage multiple storage access auth, in this case only the key will be different).

Please refer to this integration sections for more details:

 * [Data on GCS](/integrations/data-on-gcs/)
 * [Data on AWS S3](/integrations/data-on-s3/)
 * [Data on Azure storage](/integrations/data-on-azure/)
