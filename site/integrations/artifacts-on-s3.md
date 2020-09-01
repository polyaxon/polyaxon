---
title: "Artifacts on S3"
meta_title: "AWS S3"
meta_description: "Using AWS S3 buckets to organize your jobs' outputs and experiments' artifacts. Polyaxon allows users to connect to one or multiple buckets on S3 to store job outputs and experiment artifacts."
custom_excerpt: "Amazon S3 has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites."
image: "../../content/images/integrations/s3.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - artifacts
  - storage
  - aws
featured: false
popularity: 2
visibility: public
status: published
---

You can use one or multiple buckets on S3 to store logs, job outputs, and experiment artifacts.

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
artifactsStore:
  name: s3-artifacts
  kind: s3
  schema:
    bucket: "s3://bucket/"
  secret:
    name: "s3-secret"
```

## Update/Install Polyaxon deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to the artifacts store.
