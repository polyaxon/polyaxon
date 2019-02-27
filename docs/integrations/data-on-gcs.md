---
title: "Data on GCS"
meta_title: "Google GCS"
meta_description: "Using data on Google Cloud Storage GCS in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple buckets on Google Cloud Storage GCS to access data directly on you machine learning experiments."
custom_excerpt: "Google Cloud Storage is a RESTful online file storage web service for storing and accessing data on Google Cloud Platform infrastructure. The service combines the performance and scalability of Google's cloud with advanced security and sharing capabilities."
image: "../../content/images/integrations/gcs.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - data-store
  - storage
featured: true
visibility: public
status: published
---

## Create an Google cloud storage bucket

You should create a google cloud storage bucket (e.g. plx-data), and you have to assign permission to the bucket.

Google cloud storage provide an easy way to download access key as json file. You should create a secret based on that json file.

## Create a secret on Kubernetes

You should then create a secret with this access keys information on Kubernetes on the same namespace as Polyaxon deployment:

`kubectl create secret generic gcs-secret --from-file=gcs-secret.json=path/to/gcs-key.json -n polyaxon`

## Use the secret name and secret in your data persistence definition

```yaml
persistence:
  data:
    [DATA-NAME-TO-USE]:
      store: gcs
      bucket: gs://[BACKET-NAME]
      secret: [SECRET-NAME]
      secretKey: [SECRET-KEY]
```

e.g.

```yaml
persistence:
  data:
    gcs-data1:
      store: gcs
      bucket: gs://data-bucket1
      secret: gcs-secret
      secretKey: gcs-key.json
    gcs-data2:
      store: gcs
      bucket: gs://data-bucket2
      secret: gcs-secret
      secretKey: gcs-key.json
```

## Update/Install Polyaxon deployment

You can now [install](/setup/kubernetes/)/[upgrade](/setup/kubernetes/#upgrade-polyaxon) Polyaxon with access to data on GCS.

## Access to data in your experiments/jobs

You can use [polyaxon-client](/references/polyaxon-client-python/) to access the data in your jobs/experiments.

Polyaxon client does not bundle by default the google cloud storage requirements to keep the client lightweight:

```bash
pip install polyaxon-client[gcs]
``` 

or to have more control over the version of GCS storage:

```bash
pip install polyaxon-client
pip install google-cloud-storage
``` 

In your experiment/job definition, you can add this step to be available during the run:

```yaml
build:
  ...
  build_steps:
    ...
    - pip3 install polyaxon-client[gcs]
```

## Schedule data for a job/experiment

By default Polyaxon will schedule all data, volume, paths, and storages, to your experiments. If you want to control which data to be scheduled, update the environment section:

```yaml
environment:
  persistence:
    data: ['gcs-data1']
```

Exposes only `gcs-data1` to this run.


```yaml
environment:
  persistence:
    data: ['gcs-data1', 'gcs-data2', 'some-other-data-on-a-volume']
```

## Using the store manager to access data

In your experiment/job, Polyaxon exposes all secrets related to the data as well as the data [paths](/references/polyaxon-tracking-api/paths/#get-data-paths) scheduled for the run as an an env var,  
and provides an interface to get an authenticated client for each one of these Paths.

For every path in the data paths dictionary, you can create an authenticated store using the `StoreManager` 

```python
from polyaxon_client.tracking import Experiment, get_data_paths
from polystores.stores.manager import StoreManager

experiment = Experiment()
print(experiment.get_experiment_info())
# This is a dict: dataset name -> dataset info
print("Data paths: {}".format(get_data_paths()))

# e.g. one of datapaths is cifar-10
# We will create an azure client for that path
store = StoreManager(path=get_data_paths()['cifar-10'])

# Downloading train data under this blob
store.download_dir('/train')
```

All possible function to use:

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
