---
title: "Data on Azure Storage"
meta_title: "Azure Storage"
meta_description: "Using data on Azure Storage in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple blobs on Azure Storage to access data directly on your machine learning experiments and jobs."
custom_excerpt: "Azure Storage is Microsoft's cloud storage solution. Azure Storage provides storage for data objects that is highly available, secure, durable, massively scalable cloud storage solution."
image: "../../content/images/integrations/azure-storage.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - data-stores
  - storage
  - azure
featured: false
popularity: 1
visibility: public
status: published
---

You can use one or multiple blobs on Azure Storage to access data directly on your machine learning experiments and jobs.

## Create an Azure Storage account

You should create a storage account (e.g. plx-storage) and a blob (e.g. data).

You need to expose information about how to connect to the blob storage, the standard way is to expose these keys:

 * `AZURE_ACCOUNT_NAME`
 * `AZURE_ACCOUNT_KEY`
 * `AZURE_CONNECTION_STRING`

## Create a secret or a config map for storing these keys

We recommend using a secret to store your access information json object:

```bash
kubectl create secret -n polyaxon generic az-secret --from-literal=AZURE_ACCOUNT_NAME=account --from-literal=AZURE_ACCOUNT_KEY=hash-key
```

## Use the secret to add a connection

```yaml
connections:
- name: azure-dataset1
  kind: wasb
  schema:
    bucket: "wasbs://dataset1@container.blob.core.windows.net/"
  secret:
    name: "az-secret"
```

If you want ot access multiple datasets using the same secret:

```yaml
persistence:
- name: azure-dataset1
  kind: wasb
  schema:
    bucket: "wasbs://dataset1@container.blob.core.windows.net/"
  secret:
    name: "az-secret"
- name: azure-dataset2
  kind: wasb
  schema:
    bucket: "wasbs://dataset2@container.blob.core.windows.net/"
  secret:
    name: "az-secret"
```

## Update/Install Polyaxon CE or Polyaxon Agent deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to data on Azure.

## Access to the dataset in your experiments/jobs

To expose the connection secret to one of the containers in your jobs or services:

```yaml
run:
  kind: job
  connections: [azure-dataset1]
```

Or

```yaml
run:
  kind: job
  connections: [azure-dataset1, s3-dataset1]
```

## Use the initializer to load the dataset

To use the artifacts initializer to load the dataset

```yaml
run:
  kind: job
  init:
   - artifacts: {dirs: [...], files: [...]}
     connection: "azure-dataset1"
```

## Use Polyaxon to access the dataset

This is optional, you can use any language or logic to interacts with Azure Storage.

Polyaxon has some built-in logic that you can leverage if you want.

To use that logic:

```bash
pip install polyaxon[azure]
```

All possible functions to use:

```python
from polyaxon.connections.azure.azure_blobstore import AzureBlobStoreService

store = AzureBlobStoreService(...)

store.delete()
store.ls()
store.upload_file()
store.upload_dir()
store.download_file()
store.download_dir()
```
