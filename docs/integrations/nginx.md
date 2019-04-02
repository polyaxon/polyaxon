---
title: "NGINX Ingress"
meta_title: "nginx"
meta_description: "Polyaxon provides support for an Ingress resource compatible with the Nginx stable helm chart."
custom_excerpt: "NGINX Ingress Controller for Kubernetes is a controller built around the Kubernetes Ingress resource."
image: "../../content/images/integrations/nginx.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - api
featured: false
visibility: public
status: published
---

Polyaxon provides support for an Ingress resource compatible with the NGINX stable helm chart or a customized NGINX ingress controller.

## Install Nginx Ingress

In order to use NGINX Ingress controller with Polyaxon, you need install the controller w/o RBAC depending on your cluster:

```yaml
helm install -n polyaxon --name=nginx stable/nginx-ingress
```

## Enable ingress in your Polyaxon's config deployment

```yaml
ingress:
  enabled: true
```

## [Optional] Set a host name

```yaml
ingress:
  enabled: true
  hostName: polyaxon.acme.com
```

## [Optional] Set tls to serve Polyaxon on HTTPS

```yaml
ingress:
  enabled: true
  hostName: polyaxon.acme.com
  tls: 
  - secretName: polyaxon.acme-tls
    hosts:
      - polyaxon.acme.com
```

## Annotations

Polyaxon's ingress resource comes with default annotations to successfully handle some use cases:
 * Uploading/Downloading large files
 * Routing some internal services
 
You can customize further these annotations if you have some special requirements.
