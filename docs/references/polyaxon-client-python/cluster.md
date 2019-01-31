---
title: "Cluster Endpoint"
sub_link: "polyaxon-client-python/cluster"
meta_title: "Polyaxon Client Python Cluster Endpoint - Polyaxon References"
meta_description: "Polyaxon Client Python Cluster Endpoint for managing the cluster and nodes."
visibility: public
status: published
tags:
    - client
    - reference
    - polyaxon
    - sdk
    - python
    - cluster
    - management
    - orchestration
    - kubernetes
sidebar: "polyaxon-client-python"
---

## Get cluster information

```python
polyaxon_client.cluster.get_cluster()
```

## Get cluster node information

```python
# Get cluster node 1
polyaxon_client.cluster.get_node(1)
# Get cluster node 3
polyaxon_client.cluster.get_node(3)
```
