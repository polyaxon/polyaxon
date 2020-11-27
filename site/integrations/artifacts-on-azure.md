---
title: "Artifacts on Azure Storage"
meta_title: "Azure Storage"
meta_description: "Using Azure Storage to organize your jobs' outputs and experiments' artifacts. Polyaxon allows users to connect to one or multiple blobs on Azure Storage to store job outputs and experiment artifacts."
custom_excerpt: "Azure Storage is Microsoft's cloud storage solution. Azure Storage provides storage for data objects that is highly available, secure, durable, massively scalable cloud storage solution."
image: "../../content/images/integrations/azure-storage.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - artifacts
  - storage
  - azure
featured: false
popularity: 2
visibility: public
status: published
---

You can use one or multiple blobs on Azure Storage to store logs, job outputs, and experiment artifacts.

## Create an Azure Storage account

You should create a storage account (e.g. plx-storage) and a blob (e.g. artifacts).

You need to expose information about how to connect to the blob storage, the standard way is to expose these keys:

 * `AZURE_ACCOUNT_NAME`
 * `AZURE_ACCOUNT_KEY`
 * `AZURE_CONNECTION_STRING`

## Create a secret or a config map for storing these keys

We recommend using a secret to store your access information json object:

```bash
kubectl create secret -n polyaxon generic az-secret --from-literal=AZURE_ACCOUNT_NAME=account --from-literal=AZURE_ACCOUNT_KEY=hash-key
```

## Use the secret to set the artifactsStore

```yaml
artifactsStore:
  name: azure-artifacts
  kind: wasb
  schema:
    bucket: "wasbs://artifacts@container.blob.core.windows.net/"
  secret:
    name: "az-secret"
```

## Update/Install Polyaxon CE or Polyaxon Agent deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to the artifacts store.
