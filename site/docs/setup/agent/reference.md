---
title: "Helm Reference"
sub_link: "agent/reference"
meta_title: "Polyaxon Agent Helm Reference - Polyaxon References"
meta_description: "Polyaxon Agent chart is a Helm chart for creating reproducible and maintainable deployments of Polyaxon with Kubernetes."
visibility: public
status: published
tags:
    - specification
    - polyaxon
    - yaml
    - helm
    - reference
    - kubernetes
sidebar: "setup"
---

Polyaxon Agent chart is a Helm chart for deploying Polyaxon Agent on Kubernetes.

## Introduction

This chart bootstraps a Polyaxon Agent deployment on
a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

This chart can be installed on a single node or multi-nodes cluster,
in which case you need to provide some volumes with `ReadWriteMany` or cloud buckets.

> **Tip**: The full list of the default [values.yaml](https://github.com/polyaxon/polyaxon-chart/blob/master/agent/values.yaml)

## Prerequisites

- Kubernetes
- helm

## deploymentChart

| Parameter                       | Description                  | Default
| --------------------------------| ---------------------------- | ----------------------------------------------------------
| `deploymentChart`               | The deployment chart to use  | `agent`


## deploymentVersion

| Parameter                       | Description                                                                                                                                             | Default
| --------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------
| `deploymentVersion`             | The deployment version to use, this is important if you are using polyaxon-cli to avoid accidentally deploying/upgrading to a version without noticing  | `latest`


## Namespace

| Parameter                       | Description                                                                                          | Default
| --------------------------------| -----------------------------------------------------------------------------------------------------| ----------------------------------------------------------
| `namespace`                     | The namespace that will be used by Polyaxon to create operations and communicate with other services| `polyaxon`

## Gateway

The gateway is the service fronting the traffic to/from Polyaxon. By default it's deployed with `ClusterIP`.

You can use port forwarding to access the service on localhost:

```bash
kubectl port-forward -n polyaxon svc/polyaxon-polyaxon-gateway 8000:80
```

## Ingress and Gateway service

| Parameter                    | Description                                                         | Default
| ---------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------
| `ingress.enabled`            | Use Kubernetes ingress                                              | `true`
| `ingress.path`               | Kubernetes ingress path                                             | `/`
| `ingress.hostName`           | Kubernetes ingress hostName                                         | ``
| `ingress.tls`                | Use Ingress TLS (Secrets must be manually created in the namespace) | `[]`
| `ingress.annotations`        | Ingress annotations                                                 | `{}`
| `gateway.service.type`       | Gateway Service type                                                | `ClusterIP`
| `gateway.service.annotations`| Gateway Service annotations                                         | `{}`


This chart provides support for an Ingress resource.

If you enable ingress, please set the gateway service type value to:
 * ClusterIP or NodePort 
 * NodePort or LoadBalancer on GKE

Note: using TLS requires either:
 - a preconfigured secret with the TLS secrets in it
 - or the user of [cert-manager](https://github.com/helm/charts/tree/master/stable/cert-manager) to auto request certs from let's encrypt and store them in a secret.

It's also possible to use a service like [externalDNS](https://github.com/helm/charts/tree/master/stable/external-dns) to auto create the DNS entry for the polyaxon API service.

### Ingress Annotations

Example annotations:

```yaml
ingress.kubernetes.io/ssl-redirect: "false"
ingress.kubernetes.io/rewrite-target: /
ingress.kubernetes.io/add-base-url: "true"
ingress.kubernetes.io/proxy-connect-timeout: "600"
ingress.kubernetes.io/proxy-read-timeout: "600"
ingress.kubernetes.io/proxy-send-timeout: "600"
ingress.kubernetes.io/send-timeout: "600"
ingress.kubernetes.io/proxy-body-size: 4G
```

## Securing api server with TLS

If you have your own certificate you can make a new secret with the `tls.crt` and the `tls.key`,
then set the secret name in the values file.

### Automating TLS certificate creation and DNS setup

To automate the creation and registration of new domain name you can use the following services:

* [cert-manager](https://github.com/helm/charts/tree/master/stable/cert-manager)
* [externalDNS](https://github.com/helm/charts/tree/master/stable/external-dns) (Route53 / Google CloudDNS)

once installed, you can set the values for `ingress.tls`:

```yaml
ingress:
  enabled: true
  hostName: polyaxon.acme.com
  tls:
    - secretName: polyaxon.acme-tls
      hosts:
        - polyaxon.acme.com
```

TLS can have more than one host.

In order to get the domain registration to work you need to set the value of `api.service.annotations`
to the annotation needed for your domain:
i.e

```yaml
annotations:
  domainName: polyaxon.my.domain.com
```

## SSL

| Parameter | Description                                                             | Default
| ----------| ------------------------------------------------------------------------| ----------------------------------------------------------
| `ssl`     | To set ssl and serve https with Polyaxon deployed with NodePort service | `{}`


NGINX acts as a reverse proxy for the Polyaxon's front-end server, meaning NGINX proxies external HTTP (and HTTPS) requests to the Polyaxon API.

### NGINX ingress

To use Https in Polyaxon on Kubernetes you can set an ingress-nginx for cluster running on Kubernetes.

Polyaxon's helm chart comes with an ingress resource that you can use with an ingress controller where you should use TLS so that all traffic will be served over HTTPS.

 1. Create a TLS secret that contains your TLS certificate and private key.

    ```bash
    kubectl create secret tls polyaxon-tls --key $PATH_TO_KEY --cert $PATH_TO_CERT
    ```
    

 2. Add the tls configuration to Polyaxon's Ingress values. (**Do not use CluserIP on GKE**)
 
    ```yaml
    gateway:
      service:
        type: ClusterIP
    ingress:
      enabled: true
      hostName: polyaxon.acme.com
      tls:
      - secretName: polyaxon.acme-tls
        hosts:
          - polyaxon.acme.com
    ```   

    For more information visit the [Nginx Ingress Integration](/integrations/nginx/)

### NGINX for NodePort service

To enable ssl for Polyaxon API running with NodePort service on Kubernetes, you need to provide an SSL certificate and SSL certificate key.
 
you can provide a self-signed certificate or a browser trusted certificate.

 1. Create a secret for your certificate:

    ```bash
    kubectl create -n polyaxon secret generic polyaxon-cert --from-file=/path/to/certs/polyaxon.com.crt --from-file=/path/to/certs/polyaxon.com.key
    ```

 2. Make sure to update your deployment config with reference to the certificate
 
    ```yaml
    ssl:
      enabled: true  
      secretName: 'polyaxon-cert'
    ```
 3. Set the service type to `NodePort` and update the API's service port to 443.
 
 N.B. By default Polyaxon mounts the ssl certificate and key to `/etc/ssl`, this value can be updated using the `.Values.ssl.path`.

## dns

| Parameter | Description                                                             | Default
| ----------| ------------------------------------------------------------------------| ----------------------------------------------------------
| `dns`     | DNS configuration for cluster running with custom dns setup             | `{}`


Several users deploy Polyaxon on Kubernetes cluster created with [kubespray](https://github.com/kubernetes-sigs/kubespray), 
and by default Kubespray creates Kubernetes with CoreDNS as a cluster DNS server.

### Update DNS backend

Although we could provide logic to detect the DNS used in the cluster, this would require cluster wide RBAC that we think it's unnecessary. 
The default DNS backend used by Polyaxon is KubeDNS, to set it to a different DNS, you can provide this value in your Polyaxon's deployment config:

```yaml
dns:
  backend: "coredns"
```

### Update the complete DNS prefix

Since the DNS service is generally deployed on `kube-system` namespace, the default DNS prefix is `kube-dns.kube-system` or `coredns.kube-system` if you update the previous option.

You can also provide the complete DNS prefix, and not use the DNS backend options:

```yaml
dns:
  prefix: kube-dns.other-kube-system  
``` 

### Update DNS cluster

The default dns cluster used in Polyaxon to resolve routes is `cluster.local`, you can provide a Custom Cluster DNS, by setting:

```yaml
dns:
  customCluster: "custom.cluster.name"
```


## Auth

When you deploy an agent all traffic will be checked by the control plane to ensure that:

 * Users are allowed to view the content.
 * Users are authenticated to access private projects and their content.
 * That any service: Notebooks, Tensorboards, custom dashboards and apps, can be accessed following the team roles and access control configured.


| Parameter         | Description                                                   | Default
| ----------------- | ------------------------------------------------------------- | ----------------------------------------------------------
| `auth.enabled`    | To use Polyaxon auth system                                   | `true`
| `auth.useResolver`| The resolve and authenticate all traffic for managed services | `true`


## Time zone

To set a different time zone for application (convenient for the dashboard and admin interface)
you can can provide a [valid time zone value](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)


| Parameter | Description         | Default
| ----------| --------------------| ----------------------------------------------------------
| `timeZone`| The timezone to use | `UTC`


## Node manipulation

| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `nodeSelector`                     | Node selector for core pod assignment                        | `{}`
| `tolerations`                      | Tolerations for core pod assignment                          | `[]`
| `affinity`                         | Affinity for core pod assignment                             | Please check the values


### Node Selectors

Polyaxon comes with a couple of node selectors options to assign pods to nodes for polyaxon's core platform

By providing these values, or some of them,
you can constrain the pods belonging to that category to only run on
particular nodes or to prefer to run on particular nodes.

```yaml
nodeSelector:
  ...
```

### Tolerations

If one or more taints are applied to a node, and you want to make sure some pods should not deploy on it.

```yaml
tolerations:
  ...
```

### Affinity

It allows you to constrain which nodes your pod is eligible to schedule on, based on the node's labels.
Polyaxon has a default `Affinity` values for the agent's core components to ensure that they deploy on the same node.

Polyaxon's default affinity:

```yaml
affinity:
  podAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: type
              operator: In
              values:
              - "polyaxon-core"
          topologyKey: "kubernetes.io/hostname"
```

## Control Plane

```yaml
externalServices:
  api:
    host:
    port:
```

## Agent configuration

Set the agent token and instance value:

```yaml
agent:
  instance: acme.agents.UUID
  token: "TOKEN_VALUE"
```

## Security context


| Parameter                          | Description                                                  | Default
| -----------------------------------| -------------------------------------------------------------| ----------------------------------------------------------
| `securityContext.enabled`          | enable security context                                      | `false` 
| `user`                             | security context UID                                         | `2222`
| `group`                            | security context GID                                         | `2222`


Polyaxon runs all containers as root by default, this configuration is often fine for several deployment, 
however, in some use cases it can expose a compliance issue for some teams.

Polyaxon provides a simple way to enable a security context for all core components, experiments and jobs.  

Default configuration:

```yaml
securityContext:
  enabled: false
  user: 2222
  group: 2222
```

### Enable security context

```yaml
securityContext:
  enabled: true
```

or enable with custom UID/GID other than 2222/2222:

```yaml
securityContext:
  enabled: true
  user: 1111
  group: 1111
```

This will enable a security context to run all containers using a UID/GID == 1111/1111.

> If you are using a host path or a volume for the artifacts store, make sure to allow the UID/GID to access it.

## Connections

```yaml
artifactsStore: {}
connections: []
notificationConnections: []
```

You need to configure the connection to authorize for the agent. Please check [connections section](/docs/setup/connections/).
