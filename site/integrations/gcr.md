---
title: "Google GCR"
meta_title: "Google GCR"
meta_description: "How to pull images from your private Google GCR registry. Use your Google GCR (Google container registry) registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "Google Container Registry is is a fully-managed Docker container registry to store, manage, and secure your Docker container images."
image: "../../content/images/integrations/gcr.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - registry
featured: false
visibility: public
status: published
---

Integrate your Google GCR (Google container registry) with Polyaxon to start your machine learning and deep learning experiments on Kubernetes.

## Overview

You can easily add many private registries to Polyaxon to pull private images and use them when scheduling your deep learning and machine learning experiments on Kubernetes using Polyaxon.

## Enable Container Registry API

Start with enabling the Container Registry API by logging into Google Cloud and navigating to Container Registry on your project.

## Create a service account on GCS with storage admin role

 1. Go to console.cloud.google.com
 2. Make sure your project is selected
 3. Click <top-left menu w/ three horizontal bars> -> IAM & Admin -> Service Accounts menu option
 4. Click Create service account
 5. Give your account a descriptive name such as “polyaxon-gcr-access”
 6. Click Role -> Storage -> Storage Admin menu option
 7. Click Create Key
 8. Leave key type as default of JSON
 9. Click Create

## Create a secret containing the credentials to use with GCR

In order to create a valid secret using the service account key, you need to create base64 auth based on the `_json_key` and value in `json.json`.

So using python you can do:

```python
import base64
base64.b64encode('_json_key:{"type": "service_account", "project_id": "my_project", "private_key_id": "ajshvasjhqweqetquytqut17253871238", "private_key": "-----BEGIN PRIVATE KEY-----\nASBHJASJDASBDJAJHSBDJB/sfbdj1223"}'.encode())

> b'anNvbl9rZXk6eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogIm15X3Byb2plY3QiLCAicHJpdmF0ZV9rZXlfaWQiOiAiYWpzaHZhc2pocXdlcWV0cXV5dHF1dDE3MjUzODcxMjM4IiwgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLQpBU0JISkFTSkRBU0JESkFKSFNCREpCL3NmYmRqMTIyMyJ9+'
```

## Create an auths config file

```json
{
    "auths": {
        "gcr.io": {
            "auth": "anNvbl9rZXk6eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogIm15X3Byb2plY3QiLCAicHJpdmF0ZV9rZXlfaWQiOiAiYWpzaHZhc2pocXdlcWV0cXV5dHF1dDE3MjUzODcxMjM4IiwgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLQpBU0JISkFTSkRBU0JESkFKSFNCREpCL3NmYmRqMTIyMyJ9="
        }
    }
}
```
You may need to update `gcr.io`key to your repository hosts `us.gcr.io`, `eu.gcr.io`, or `asia.gcr.io` if you are using not default one.

## Create a secret with config.json as a name

```bash
kubectl create secret generic docker-conf --from-file=config.json=./config.json -n polyaxon
```

## Add the secret to the k8s_secrets catalog in Stores

In order to use secret that you created before, in Polyaxon's Stores > Secrets, create a new secret entry, and set name and K8S Ref to "docker-conf".

## Create a docker registry access in the UI

In Polyaxon's stores, add a new entry and link to secret that you created at previous step, and set the host to `gcr.io/my-project`, `us.gcr.io/my-project`, `eu.gcr.io/my-project`, or `asia.gcr.io/my-project`.

![access](../../content/images/integrations/docker-access.png)


## Make this access as default

After creating the access you need to mark it as default, so that Polyaxon uses it for scheduling builds. 


## Using the secret for pull only

If you wish to only use this credential secret for pulling images and the in-cluster registry for pushing, you should leave the host field empty.

## You can allow the docker process to pull from different registries

To allow this access to pull from other registries, you can set as many other auths and credsStore.
