---
title: "Polyaxon Cluster Rest API"
sub_link: "polyaxon-api/cluster"
meta_title: "Polyaxon Cluster Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Cluster Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - cluster
    - orchestration
sidebar: "polyaxon-api"
---

## Get cluster information

<span class="api api-get">
/api/v1/cluster/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://localhost:8000/api/v1/cluster \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

### Example responses

```json
{
    "uuid": "2d78d354419d4ff2b1eac1c6333cb197",
    "version_api": {
        "major": "1",
        "go_version": "go1.9.3b4",
        "platform": "linux/amd64",
        "git_version": "v1.10.6-gke.1",
        "minor": "10+",
        "compiler": "gc",
        "build_date": "2018-08-08T18:09:40Z",
        "git_commit": "ee18aa41359293b5c9c7e13a35697690491736c9",
        "git_tree_state": "clean"
    },
    "created_at": "2018-08-19T21:59:47.519000+02:00",
    "updated_at": "2018-08-19T22:03:36.870000+02:00",
    "nodes": [
        {
            "uuid": "ab71a5a6f5044154b8e743bc393d0f4b",
            "sequence": 3,
            "name": "gke-cluster-1-default-pool-65d093c7-g98s",
            "hostname": "gke-cluster-1-default-pool-65d093c7-g98s",
            "role": "agent",
            "memory": 5910790144,
            "cpu": 1.93,
            "n_gpus": 0
        },
        {
            "uuid": "38d81ef8f96648049d81bc266d43444d",
            "sequence": 2,
            "name": "gke-cluster-1-default-pool-65d093c7-f096",
            "hostname": "gke-cluster-1-default-pool-65d093c7-f096",
            "role": "agent",
            "memory": 5910781952,
            "cpu": 1.93,
            "n_gpus": 0
        },
        {
            "uuid": "6948eaf67f5b4e78b698c471eb484ee3",
            "sequence": 1,
            "name": "gke-cluster-1-default-pool-65d093c7-7hk4",
            "hostname": "gke-cluster-1-default-pool-65d093c7-7hk4",
            "role": "agent",
            "memory": 5910790144,
            "cpu": 1.93,
            "n_gpus": 0
        }
    ]
}
```

## Get cluster node information

<span class="api api-get">
/api/v1/nodes/{sequence}
</span>


<b>Example curl request</b>

```
curl -X GET \
  http://localhost:8000/api/v1/nodes/{{sequence}} \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

### Example responses

```json
{
    "uuid": "6948eaf67f5b4e78b698c471eb484ee3",
    "gpus": [],
    "sequence": 1,
    "name": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "hostname": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "role": "agent",
    "docker_version": "17.3.2",
    "kubelet_version": "v1.10.6-gke.1",
    "os_image": "Ubuntu 16.04.5 LTS",
    "kernel_version": "4.15.0-1015-gcp",
    "schedulable_taints": true,
    "schedulable_state": true,
    "memory": 5910790144,
    "cpu": 1.93,
    "n_gpus": 0,
    "status": "ready",
    "is_current": true
}
```
