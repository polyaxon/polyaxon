---
title: "Outputs on Minio"
meta_title: "Minio"
meta_description: "Using Minio buckets to organize your jobs outputs and experiment artifacts. Polyaxon allows users to connect to one or multiple buckets on Minio to store job outputs and experiment artifacts."
custom_excerpt: "Minio is a high performance distributed object storage server, designed for large-scale private cloud infrastructure."
image: "../../content/images/integrations/minio.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - artifacts
  - storage
featured: false
popularity: 1
visibility: public
status: published
---

Polyaxon allows users to connect to one or multiple buckets on Minio to store job outputs and experiment artifacts.

## Deploy Minio

Before using Minio, you need to deployed it and create a bucket to host your outputs.

For that you can use the Helm stable chart: `helm install stable/minio --name=plx-minio --namespace=polyaxon`

## Create a bucket on Minio

You should create a bucket (e.g. plx-outputs) where you will host your outputs. 

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

`kubectl create secret generic s3-secret --from-file=s3-secret.json=path/to/s3-key.json -n polyaxon`


## Use the secret name and secret key in your outputs persistence definition

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

You can [deploy](/docs/setup/connections/) Polyaxon with access the outputs on S3.

## Storing outputs and artifacts in your experiments/jobs

You can use [polyaxon-client](/docs/core/python-library/) to access the outputs in your jobs/experiments.

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

In your experiment/job, Polyaxon exposes the secret related to the outputs as well as the outputs [path](/docs/experimentation/tracking/in-cluster/#get-outputs-path) scheduled for the run as an an env var,  
and provides an interface to get an authenticated client for each one of these Paths.

```python
from polyaxon_client.tracking import Experiment

experiment = Experiment()
...
experiment.log_artifact(file_path)
experiment.log_artifacts(dir_path)
``` 
