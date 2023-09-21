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

## Access the dataset programmatically

This is optional, you can use any language or logic to interact with Azure Blob Storage buckets.

For instance you can install `Azure Blob Storage Python SDK` and it will be configured automatically when you request the Azure Blob Storage connection.

You can also use Polyaxon's fs library to get a fully resolved [adlfs](https://github.com/fsspec/adlfs) instance:

```bash
pip install polyaxon[azure]
```

Creating a sync instance of the adlfs client:

```python
from polyaxon.fs import get_fs_from_name

...
fs = get_fs_from_name("azure-dataset1")  # You can pass additional kwargs to the function
...
```

Creating an async instance of the adlfs client:

```python
from polyaxon.fs import get_fs_from_name

...
fs = get_fs_from_name("azure-dataset1",
                      asynchronous=True)  # You can pass additional kwargs to the function
...
```
