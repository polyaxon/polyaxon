---
title: "Customize repos storage"
sub_link: "custom-repos-storage"
meta_title: "Customize Repos Volumes in Polyaxon - Configuration"
meta_description: "Polyaxon allows to use volumes for storing code repos."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
    - environment
    - orchestration
    - volumes
sidebar: "configuration"
---

Polyaxon allows to mount a volume to store repos.

## Default behaviour

When the user does not provide any repos configuration, the default behaviour is to use a local path on the host node for storing repos, 
this behaviour allows Polyaxon deployment to finish successfully cases without raising any errors.

Often times this default value is sufficient for users who are just trying the platform, and don't want to deal with configuration steps.

## Chart Definition

The [helm reference](/references/polyaxon-helm-reference/#persistence) describes briefly the repos persistence definitions,
and how you can mount volumes and persistent claims:


```yaml
persistence:
  repos:
    ...
```

For a multi-nodes deployment we recommend using `ReadWriteMany` persistent volume.

## Host paths

You can use host paths to define a repos storage:

```yaml
persistence:
  repos:
    mountPath: "/polyaxon-repos"
    hostPath: "/path/to/logs"
```

Users must know when to use host paths, we do not recommend this option for a multi-nodes deployment, 
because several Polyaxon components might not be able to access the logs to function correctly if they are scheduled on different nodes.

Users should be aware as well, that by losing the node where the host path is defined, all logs will be lost as well.

## Persistent Volumes

You can use a [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to store your repos:

```yaml
persistence:
  logs:
    mountPath: "/polyaxon-repos"
    existingClaim: "logs-pvc"
```

If you are using a persistent volume with one node access you need to be aware that some Polyaxon components must be scheduled on the same node.

Users must know when to use a single access volume, we do not recommend this option for a multi-nodes deployment where the API, scheduler, are replicated over multiple nodes, 
because several Polyaxon components might not be able to access the logs to function correctly if they are scheduled on different nodes.

There are some options that support multi-nodes access, e.g. a PVC backed with an NFS/Glusterfs server, 
where you can use multiple nodes, this allows you to easily scale your API, scheduler and have access to read and write repos. 
Please refer to [this section](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) to learn more about access modes.


## External repos

If you are using a code management platform, e.g. Github, Bitbucket, GitLab, to track your code, it's often time less problematic to lose code, because the commit will be hosted on that code management Platform.
