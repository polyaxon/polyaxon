---
title: "Data on Minio"
meta_title: "Minio"
meta_description: "Using data on Minio in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple buckets on Minio to access data directly on you machine learning experiments."
custom_excerpt: "Minio is a high performance distributed object storage server, designed for large-scale private cloud infrastructure."
image: "../../content/images/integrations/minio.png"
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

Polyaxon allows users to connect to one or multiple buckets on Minio to access data directly on you machine learning experiments and jobs.

## Deploy Minio

Before using Minio, you need to deployed it and create a bucket (or several) to host your data.

For that you can use the Helm stable chart: `helm install stable/minio --name=plx-minio --namespace=polyaxon`

## Create a bucket on Minio

You should create a bucket (e.g. plx-storage) where you will host your data. 

In order to use the buckets with Polyaxon, you should create a file containing your access information json object, e.g. `minio-s3-key.json`.
This file should include at least the following information:

```json
{
  "AWS_ENDPOINT_URL": "", 
  "AWS_ACCESS_KEY_ID" : "",
  "AWS_SECRET_ACCESS_KEY": ""
}
```

When Minio is installed via Helm with default values, it uses the following hard-wired default credentials, which you will use to login to the UI and setup access to Polyaxon:

```
AccessKey: AKIAIOSFODNN7EXAMPLE
SecretKey: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Your secret content will be:

```json
{
  "AWS_ENDPOINT_URL": "http://plx-minio:9000",
  "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
  "AWS_SECRET_ACCESS_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}
```

## Create a secret for accessing Minio

You should then create a secret with this access keys information on Kubernetes on the same namespace as Polyaxon deployment:

`kubectl create secret generic s3-secret --from-file=s3-secret.json=path/to/minio-s3-key.json -n polyaxon`

## Use the secret name and secret key in your data persistence definition

```yaml
persistence:
  data:
    [DATA-NAME-TO-USE]:
      store: s3
      bucket: s3://[BUCKET-NAME]
      secret: [SECRET-NAME]
      secretKey: [SECRET-KEY]
```

e.g. If you created 2 buckets on Minio for your data: `data1-bucket` and `data2-bucket` your persistence will be:

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

You can [deploy](/docs/setup/connections/) Polyaxon with access to data on Minio.

## Access to data in your experiments/jobs

You can use [polyaxon-client](/docs/core/python-library/) to access the data in your jobs/experiments.

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
  data_refs: ['s3-data1']
```

Exposes only `s3-data1` to this run.


```yaml
environment:
  data_refs: ['s3-data1', 's3-data2', 'some-other-data-on-a-volume']
```

## Using the store manager to access data

In your experiment/job, Polyaxon exposes all secrets related to the data as well as the data [paths](/docs/experimentation/tracking/in-cluster/#get-data-paths) scheduled for the run as an an env var, 
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
