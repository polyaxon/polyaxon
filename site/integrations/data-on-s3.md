---
title: "Data on S3"
meta_title: "AWS S3"
meta_description: "Using data on AWS S3 in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple buckets on S3 to access data directly on your machine learning experiments and jobs."
custom_excerpt: "Amazon S3 has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites."
image: "../../content/images/integrations/s3.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - data-stores
  - storage
  - aws
featured: true
popularity: 1
visibility: public
status: published
---

You can use one or multiple buckets on S3 to access data directly on your machine learning experiments and jobs.

## Create an S3 bucket

You should create an S3 bucket (e.g. plx-storage).

You need to expose information about how to connect to the blob storage, the standard way is to expose these keys:

 * `AWS_ACCESS_KEY_ID`
 * `AWS_SECRET_ACCESS_KEY`

And optionally these keys:
 * `AWS_ENDPOINT_URL`
 * `AWS_ACCESS_KEY_ID`
 * `AWS_SECRET_ACCESS_KEY`
 * `AWS_SECURITY_TOKEN`
 * `AWS_REGION`

## Create a secret or a config map for storing these keys

We recommend using a secret to store your access information json object:

```bash
kubectl create secret -n polyaxon generic s3-secret --from-literal=AWS_ACCESS_KEY_ID=key-id --from-literal=AWS_SECRET_ACCESS_KEY=hash-key
```

## Use the secret name and secret key in your data persistence definition

```yaml
connections:
- name: s3-dataset1
  kind: s3
  schema:
    bucket: "s3://bucket/"
  secret:
    name: "s3-secret"
```

If you want ot access multiple datasets using the same secret:

```yaml
connections:
- name: s3-dataset1
  kind: s3
  schema:
    bucket: "s3://bucket/path1"
  secret:
    name: "s3-secret"
- name: s3-dataset1
  kind: s3
  schema:
    bucket: "s3://bucket/path2"
  secret:
    name: "s3-secret"
```

## Update/Install Polyaxon deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to data on S3.

## Access to the dataset in your experiments/jobs

To expose the connection secret to one of the containers in your jobs or services:

```yaml
run:
  kind: job
  connections: [s3-dataset1]
```

Or

```yaml
run:
  kind: job
  connections: [s3-dataset1, azure-dataset1]
```

## Use the initializer to load the dataset

To use the artifacts initializer to load the dataset

```yaml
run:
  kind: job
  init:
   - artifacts: {dirs: [...], files: [...]}
     connection: "s3-dataset1"
```

## Access the dataset programmatically

This is optional, you can use any language or logic to interact with S3 buckets.

For instance you can install `boto3` and it will be configured automatically when you request the S3 connection.

You can also use Polyaxon's fs library to get a fully resolved [s3fs](https://s3fs.readthedocs.io/en/latest/) instance:

```bash
pip install polyaxon[s3]
```

Creating a sync instance of the s3fs client:

```python
from polyaxon.fs import get_fs_from_name

...
fs = get_fs_from_name("s3-dataset1")  # You can pass additional kwargs to the function
...
```

Creating an async instance of the s3fs client:

```python
from polyaxon.fs import get_fs_from_name

...
fs = get_fs_from_name("s3-dataset1",
                      asynchronous=True)  # You can pass additional kwargs to the function
...
```
