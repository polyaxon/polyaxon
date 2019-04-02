---
title: "Custom cluster DNS configuration"
sub_link: "custom-dns"
meta_title: "Custom cluster DNS setup in Polyaxon - Configuration"
meta_description: "Polyaxon's NGINX HTTP and HTTPS/SSL configuration."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - dns
sidebar: "configuration"
---

Several users deploy Polyaxon on Kubernetes cluster create with [kubespray](https://github.com/kubernetes-sigs/kubespray), 
and by default Kubespray creates Kubernetes with CoreDNS as a cluster DNS server.

Prior to v0.4.3, Polyaxon did not support Kubernetes cluster with CoreDNS, and we recommended to our users to customize their Kubernetes installation to use KubeDNS.

Starting from v0.4.3, Polyaxon provides support to CoreDNS as well as any DNS setup, by exposing some configurable options. 

## Update DNS backend

Although we could provide logic to detect the DNS used in the cluster, this would require cluster wide RBAC that we think it's unnecessary. 
The default DNS backend used by Polyaxon is KubeDNS, to set it to a different DNS, you can provide this value in you Polyaxon's deployment config:

```yaml
dns:
  backend: "coredns"
```

## Update complete DNS prefix

Since the DNS service is generally deployed on `kube-system` namespace, the default DNS prefix is `kube-dns.kube-system` or `coredns.kube-system` is you update the previous option.

You can also provide the whole DNS prefix, and not use the DNS backend options:

```yaml
dns:
  prefix: kube-dns.other-kube-system  
``` 

## Update DNS cluster

The default dns cluster used in Polyaxon to resolve routes is `cluster.local`, you can provide a Custom Cluster DNS, by setting:

```yaml
dns:
  customCluster: "custom.cluster.name"
```
