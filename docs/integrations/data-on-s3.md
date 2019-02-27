---
title: "Data on S3"
meta_title: "AWS S3"
meta_description: "Using data on AWS S3 in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple buckets on S3 to access data directly on you machine learning experiments."
custom_excerpt: "Amazon S3 has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites."
image: "../../content/images/integrations/s3.png"
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

## Create an S3 bucket

You should create an S3 bucket (e.g. plx-storage). 

In order to use S3 buckets with Polyaxon, you should create a file containing your access information json object, e.g. `s3-key.json`.
This file should include at least the following information:

```json
{
  "AWS_ACCESS_KEY_ID" : "",
  "AWS_SECRET_ACCESS_KEY": ""
}
```

All possible values:

```json
{
  "AWS_ENDPOINT_URL": "",
  "AWS_ACCESS_KEY_ID": "",
  "AWS_SECRET_ACCESS_KEY": "",
  "AWS_SECURITY_TOKEN": "",
  "AWS_REGION": ""
}
```

## Create a secret on Kubernetes

You should then create a secret with this access keys information on Kubernetes on the same namespace as Polyaxon deployment:

`kubectl create secret generic s3-secret --from-file=s3-secret.json=path/to/s3-key.json -n polyaxon`

## Use the secret name and secret in your data persistence definition

```yaml
persistence:
  data:
    [DATA-NAME-TO-USE]:
      store: s3
      bucket: s3://[BUCKET-NAME]
      secret: [SECRET-NAME]
      secretKey: [SECRET-KEY]
```

e.g.

```yaml
persistence:
  data:
    s3-data1:
      store: s3
      bucket: s3://data1-bucket
      secret: s3-secret
      secretKey: s3-key
    s3-data2:
      store: s3
      bucket: s3://data2-bucket
      secret: s3-secret
      secretKey: s3-secret.json
```

## Update/Install Polyaxon deployment

You can now [install](/setup/kubernetes/)/[upgrade](/setup/kubernetes/#upgrade-polyaxon) Polyaxon with access to data on S3.

## Access to data in your experiments/jobs

You can use [polyaxon-client](/references/polyaxon-client-python/) to access the data in your jobs/experiments.

Polyaxon client does not bundle by default the S3 storage requirements to keep the client lightweight:

```bash
pip install polyaxon-client[s3]
``` 

or to have more control over the version of S3 storage:

```bash
pip install polyaxon-client
pip install boto3
pip install botocore
``` 

In your experiment/job definition, you can add this step to be available during the run:

```yaml
build:
  ...
  build_steps:
    ...
    - pip3 install polyaxon-client[s3]
```

## Schedule data for a job/experiment

By default Polyaxon will schedule all data, volume, paths, and storages, to your experiments. If you want to control which data to be scheduled, update the environment section:

```yaml
environment:
  persistence:
    data: ['s3-data1']
```

Exposes only `s3-data1` to this run.


```yaml
environment:
  persistence:
    data: ['s3-data1', 's3-data2', 'some-other-data-on-a-volume']
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
