---
title: "Outputs on S3"
meta_title: "AWS S3"
meta_description: "Using AWS S3 buckets to organize your jobs outputs and experiment artifacts. Polyaxon allows users to connect to one or multiple buckets on S3 to store job outputs and experiment artifacts."
custom_excerpt: "Amazon S3 has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites."
image: "../../content/images/integrations/s3.png"
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

## Use the secret name and secret in your outputs persistence definition

```yaml
persistence:
  outputs:
    [OUTPUTS-NAME-TO-USE]:
      store: s3
      bucket: s3://[BUCKET-NAME]
      secret: [SECRET-NAME]
      secretKey: [SECRET-KEY]
```

e.g.

```yaml
persistence:
  outputs:
    outputs:
      store: s3
      bucket: s3://outputs-bucket
      secret: s3-secret
      secretKey: s3-key
```

## Update/Install Polyaxon deployment

You can now [install](/setup/kubernetes/)/[upgrade](/setup/kubernetes/#upgrade-polyaxon) Polyaxon with access the outputs on S3.

## Storing outputs and artifacts in your experiments/jobs

You can use [polyaxon-client](/references/polyaxon-client-python/) to access the outputs in your jobs/experiments.

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

## Tensorflow

If you are using Tensorflow, you won't need to do any further configuration since Tensorflow can natively use S3, 
Polyaxon will automatically set the required environment variables so that Tensorflow can use the bucket. 
