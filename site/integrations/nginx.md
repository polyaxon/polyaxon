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
  - setup
featured: false
popularity: 0
visibility: public
status: published
---

Polyaxon provides support for an Ingress resource compatible with the NGINX stable helm chart or a customized NGINX ingress controller.

## Install Nginx Ingress

In order to use NGINX Ingress controller with Polyaxon, you need to install the controller w/o RBAC depending on your cluster:

```yaml
helm repo add nginx-stable https://helm.nginx.com/stable
helm install nginx nginx-stable/nginx-ingress -n polyaxon
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

> **Note**: Depending on your version of nginx ingress you may need to prepend `nginx.` to the annotations. E.g.:
> ```yaml
>       nginx.ingress.kubernetes.io/proxy-body-size: 4G
>       # instead of
>       ingress.kubernetes.io/proxy-body-size: 4G
> ```

Polyaxon's ingress resource can be customized by providing annotations, we recommend the following annotations

```yaml
ingress:
  annotations:
    ingress.kubernetes.io/rewrite-target: /
    ingress.kubernetes.io/add-base-url: "true"
```

If you are using the ingress without a tls, you need to set

```yaml
ingress:
  annotations:
    ingress.kubernetes.io/ssl-redirect: "false"
```

Also to allow the platform to upload/download large files you need to

```yaml
ingress:
  annotations:
    ingress.kubernetes.io/proxy-connect-timeout: "600"
    ingress.kubernetes.io/proxy-read-timeout: "600"
    ingress.kubernetes.io/proxy-send-timeout: "600"
    ingress.kubernetes.io/send-timeout: "600"
    ingress.kubernetes.io/proxy-body-size: 4G
```

You might also need to specify the class

```yaml
ingress:
  annotations:
    kubernetes.io/ingress.class: nginx
```

## ConfigMap for the controller

In addition to the previous annotations, you may need to update the controller's config map:

```yaml
data:
  ssl-redirect: "false"
```
