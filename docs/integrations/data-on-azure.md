---
title: "Data on Azure Storage"
meta_title: "Azure Storage"
meta_description: "Using data on Azure Storage in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple blobs on Azure Storage to access data directly on you machine learning experiments."
custom_excerpt: "Azure Storage is Microsoft's cloud storage solution. Azure Storage provides storage for data objects that is highly available, secure, durable, massively scalable cloud storage solution."
image: "../../content/images/integrations/azure-storage.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - data-store
  - storage
featured: false
visibility: public
status: published
---

## Create an Azure Storage account

You should create a storage account (e.g. plx-storage) and a blob (e.g. data). 
You should then create a file with your access information json object, e.g. `az-key.json`. 
This file should include the following information:

```json
{ 
  "AZURE_ACCOUNT_NAME": "plx-storage",
  "AZURE_ACCOUNT_KEY": "your key",
  "AZURE_CONNECTION_STRING": "your connection string",
}
```

## Create a secret on Kubernetes

You should then create a secret with this access keys information on Kubernetes on the same namespace as Polyaxon deployment:

`kubectl create secret generic az-secret --from-file=az-secret.json=path/to/az-key.json -n polyaxon`

## Use the secret name and secret in your data persistence definition

```yaml
persistence:
  data:
    [DATA-NAME-TO-USE]:
      store: azure
      bucket: wasbs://[CONTAINER-NAME]@[ACCOUNT-NAME].blob.core.windows.net/
      secret: [SECRET-NAME]
      secretKey: [SECRET-KEY]
```

e.g.

```yaml
persistence:
  data:
    azure-data1:
      store: azure
      bucket: wasbs://data1@account.blob.core.windows.net/
      secret: az-secret
      secretKey: az-secret.json
    azure-data2:
      store: azure
      bucket: wasbs://data2@account.blob.core.windows.net/
      secret: az-secret
      secretKey: az-secret.json
```

## Update/Install Polyaxon deployment

You can now [install](/setup/kubernetes/)/[upgrade](/setup/kubernetes/#upgrade-polyaxon) Polyaxon with access to data on Azure.

## Access to data in your experiments/jobs

You can use [polyaxon-client](/references/polyaxon-client-python/) to access the data in your jobs/experiments.

Polyaxon client does not bundle by default the azure storage requirements to keep the client lightweight:

```bash
pip install polyaxon-client[azure]
``` 

or to have more control over the version of azure storage:

```bash
pip install polyaxon-client
pip install azure-storage
``` 

In your experiment/job definition, you can add this step to be available during the run:

```yaml
build:
  ...
  build_steps:
    ...
    - pip3 install polyaxon-client[azure]
```

## Schedule data for a job/experiment

By default Polyaxon will schedule all data, volume, paths, and storages, to your experiments. If you want to control which data to be scheduled, update the environment section:

```yaml
environment:
  persistence:
    data: ['azure-data1']
```

Exposes only `azure-data1` to this run.


```yaml
environment:
  persistence:
    data: ['azure-data1', 'azure-data2', 'some-other-data-on-a-volume']
```

## Using the store manager to access data

In your experiment/job, Polyaxon exposes all secrets related to the data as well as the data [paths](/references/tracking-api/paths/#get-data-paths) scheduled for the run as an an env var, 
and provides an interface to get an authenticated client for each one of these Paths.

For every path in the data paths dictionary, you can create an authenticated store using the `StoreManager` 

```python
from polystores.stores.manager import StoreManager

store = StoreManager(path=data_path)

store.delete(path)
store.ls(path)
store.upload_file(filename)
store.upload_dir(dirname)
store.download_file(filename, local_path)
store.download_dir(dirname, local_path)
```
