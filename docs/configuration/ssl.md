---
title: "SSL https configuration"
sub_link: "ssl"
meta_title: "SSL https configuration in Polyaxon - Configuration"
meta_description: "Polyaxon's NGINX HTTP and HTTPS/SSL configuration."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
    - ssl
    - https
sidebar: "configuration"
---

NGINX acts as a reverse proxy for the Polyaxon's front-end server, meaning NGINX proxies external HTTP (and HTTPS) requests to the Polyaxon API.

## NGINX for Polyaxon Cluster (Kubernetes)

The recommended way to use Https in Polyaxon on Kubernetes is by setting an ingress-nginx for the Polyaxon Cluster running on Kubernetes.

Polyaxon's helm chart comes with an ingress resource that you can use with an ingress controller where you should use TLS so that all traffic will be served over HTTPS.

 1. Create a TLS secret that contains your TLS certificate and private key.

    ```bash
    kubectl create secret tls polyaxon-tls --key $PATH_TO_KEY --cert $PATH_TO_CERT
    ```
    

 2. Add the tls configuration to Polyaxon's Ingress values. (**Do not use CluserIP on GKE**)
 
    ```yaml
    serviceType: ClusterIP
    ingress:
      enabled: true
      hostName: polyaxon.acme.com
      tls:
      - secretName: polyaxon.acme-tls
        hosts:
          - polyaxon.acme.com
    ```   

    For more information visit the [Nginx Ingress Integration](/integrations/nginx/)

## NGINX for Polyaxon running with a NodePort service

To enable ssl for Polyaxon API running with NodePort service on Kubernetes, you need to provide an ssl certificate and ssl certificate key.
 
you can provide a self-signed certificate or a browser trusted certificate.

 1. Create a secret for you certificate:

    ```bash
    kubectl create -n polyaxon secret generic polyaxon-cert --from-file=/path/to/certs/polyaxon.com.crt --from-file=/path/to/certs/polyaxon.com.key
    ```

 2. Make sure to update you deployment config with reference to the certificate
 
    ```yaml
    ssl:
      enabled: true  
      secretName: 'polyaxon-cert'
    ```
 3. Set the service type to `NodePort` and update the api's service port to 443.
 
 N.B. By default Polyaxon mounts the ssl certificate and key to `/etc/ssl`, this value can be updated using the `.Values.ssl.path`.

## NGINX for Polyaxon single instance (docker) or Docker Compose

The process for using certificate with a Polyaxon deployment on docker or docker compose is quite similar to kubernetes's NodePort service, 
you need to mount an ssl certificate and ssl certificate key to `/etc/ssl`, and set `POLYAXON_NGINX_ENABLE_SSL` to true/1.

## CLI setup

If you are serving Polyaxon on HTTPS, you should be aware that CLI need to have a different config:

```bash
polyaxon config set --host=IP/Host --port=443 --use_https=true [--verify_ssl]
```
