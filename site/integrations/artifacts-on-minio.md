---
title: "Artifacts on Minio"
meta_title: "Minio"
meta_description: "Using Minio buckets to organize your jobs' outputs and experiments' artifacts. Polyaxon allows users to connect to one or multiple buckets on Minio to store job outputs and experiment artifacts."
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

You can use one or multiple buckets on Minio to store logs, job outputs, and experiment artifacts.

## Deploy Minio

Before using Minio, you need to deploy it and create a bucket to host your outputs.

There are different ways to deploy [Minio on Kubernetes](https://docs.min.io/docs/deploy-minio-on-kubernetes), 
if you want to deploy Minio using the Helm Chart, you need to:

 * Add Minio's repo:
 
```bash
helm install stable/minio
```

 * Deploy Minio's chart:

```bash
helm install plx-minio minio/minio --namespace=polyaxon
```

You can also deploy with different configuration by using a config.yaml or passing the values as params, e.g. `--set accessKey=myaccesskey,secretKey=mysecretkey`

## Create a bucket on Minio

You should create a bucket (e.g. plx-artifacts) where you will host your data.

## Use the bucket in Polyaxon

In order to use the buckets with Polyaxon, you can follow the [S3 Artifacts integration](/integrations/artifacts-on-s3/).


> **Note**: When Minio is installed via Helm with default values, it uses the following hard-wired default credentials, which you will use to login to the UI and setup access to Polyaxon:

```
AccessKey: myaccesskey
SecretKey: mysecretkey
```

This means that the default secret keys should be:

 * AWS_ENDPOINT_URL: "http://plx-minio:9000"
 * AWS_ACCESS_KEY_ID: "myaccesskey",
 * AWS_SECRET_ACCESS_KEY: "mysecretkey"
