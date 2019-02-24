---
title: "Outputs on Azure Storage"
meta_title: "Azure Storage"
meta_description: "Using Azure Storage to organize your jobs outputs and experiment artifacts. Polyaxon allows users to connect to one or multiple blobs on Azure Storage to store job outputs and experiment artifacts."
custom_excerpt: "Azure Storage is Microsoft's cloud storage solution. Azure Storage provides storage for data objects that is highly available, secure, durable, massively scalable cloud storage solution."
image: "../../content/images/integrations/azure-storage.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - artifacts-store
  - storage
featured: false
visibility: public
status: published
---

## Create an Azure Storage account

You should create a storage account (e.g. plx-storage) and a blob (e.g. outputs). 
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

## Use the secret name and secret in your outputs persistence definition

```yaml
persistence:
  outputs:
    [OUTPUTS-NAME-TO-USE]:
      store: azure
      bucket: wasbs://[CONTAINER-NAME]@[ACCOUNT-NAME].blob.core.windows.net/
      secret: [SECRET-NAME]
      secretKey: [SECRET-KEY]
```

e.g.

```yaml
persistence:
  outputs:
    outputs:
      store: azure
      bucket: wasbs://outputs@account.blob.core.windows.net/
      secret: az-secret
      secretKey: az-secret.json
```

## Update/Install Polyaxon deployment

You can now [install](/setup/kubernetes/)/[upgrade](/setup/kubernetes/#upgrade-polyaxon) Polyaxon with access the outputs on Azure.

## Storing outputs and artifacts in your experiments/jobs

You can use [polyaxon-client](/references/polyaxon-client-python/) to access the outputs in your jobs/experiments.

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

## Using the outputs store from tracking

In your experiment/job, Polyaxon exposes the secret related to the outputs as well as the outputs [path](/references/polyaxon-tracking-api/paths/#get-outputs-path) scheduled for the run as an an env var, 
and provides an interface to get an authenticated client for each one of these Paths.

```python
from polyaxon_client.tracking import Experiment

experiment = Experiment()
...
experiment.outputs_store.upload_file(file_path)
experiment.outputs_store.upload_dir(dir_path)
``` 
