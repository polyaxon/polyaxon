---
title: "Data on GCS"
meta_title: "Google GCS"
meta_description: "Using data on Google Cloud Storage GCS in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple buckets on Google Cloud Storage GCS to access data directly on your machine learning experiments and jobs."
custom_excerpt: "Google Cloud Storage is a RESTful online file storage web service for storing and accessing data on Google Cloud Platform infrastructure. The service combines the performance and scalability of Google's cloud with advanced security and sharing capabilities."
image: "../../content/images/integrations/gcs.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - data-stores
  - storage
  - gcp
featured: true
popularity: 1
visibility: public
status: published
---

You can use one or multiple buckets on Google Cloud Storage (GCS) to access data directly on your machine learning experiments and jobs.

## Create a Google cloud storage bucket

You should create a google cloud storage bucket (e.g. plx-data), and you have to assign permission to the bucket.

Google cloud storage provides an easy way to download the access key as a JSON file. You should create a secret based on that JSON file.

## Create a secret on Kubernetes

You can create a secret with an env var of the content of the gcs-key.json:
 * `GC_KEYFILE_DICT` or `GOOGLE_KEYFILE_DICT`

Or you can create a secret to be mounted as a volume:

 * `kubectl create secret generic gcs-secret --from-file=gc-secret.json=path/to/gcs-key.json -n polyaxon`

## Use the secret name and secret key in your data persistence definition

You can use the default mount path `/plx-context/.gc`, Polyaxon will set the `GC_KEY_PATH` to `/plx-context/.gc/gc-secret.json` so the secret must contain --from-file=`gc-secret.json=`

```yaml
connections:
- name: gcs-dataset1
  kind: gcs
  schema:
    bucket: "gs://gcs-datasets"
  secret:
    name: "gcs-secret"
    mountPath: /plx-context/.gc
```

You can also use a different mount path `/etc/gcs`, in which case you need to provide an env var to tell the SDK where to look:

```bash
kubectl create configmap gcs-key-path --from-literal GC_KEY_PATH="/etc/gcs/gc-secret.json" -n polyaxon
```

```yaml
connections:
- name: gcs-dataset1
  kind: gcs
  schema:
    bucket: "gs://gcs-datasets"
  secret:
    name: "gcs-secret"
    mountPath: /etc/gcs
  configMap:
    name: gcs-key-path
```

If you want ot access multiple datasets using the same secret:

```yaml
persistence:
- name: gcs-dataset1
  kind: gcs
  schema:
    bucket: "gs://gcs-datasets/path1"
  secret:
    name: "gcs-secret"
    mountPath: /etc/gcs
  configMap:
    name: gcs-key-path
- name: gcs-dataset2
  kind: gcs
  schema:
    bucket: "gs://gcs-datasets/path2"
  secret:
    name: "gcs-secret"
    mountPath: /etc/gcs
  configMap:
    name: gcs-key-path
```

## Update/Install Polyaxon deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to data on GCS.

## Access to data in your experiments/jobs

To expose the connection secret to one of the containers in your jobs or services:

```yaml
run:
  kind: job
  connections: [gcs-dataset1]
```

Or

```yaml
run:
  kind: job
  connections: [gcs-dataset1, s3-dataset1]
```

## Use the initializer to load the dataset

To use the artifacts initializer to load the dataset

```yaml
run:
  kind: job
  init:
   - artifacts: {dirs: [...], files: [...]}
     connection: "gcs-dataset1"
```

## Access the dataset programmatically

This is optional, you can use any language or logic to interact with Google Cloud Storage buckets.

For instance you can install `gcloud` CLI and it will be configured automatically when you request the GCS connection.

You can also use Polyaxon's fs library to get a fully resolved [gcsfs](https://gcsfs.readthedocs.io/en/latest/) instance:

To use that logic:

```bash
pip install polyaxon[gcs]
```

Creating a sync instance of the gcsfs client:

```python
from polyaxon.fs import get_fs_from_name

...
fs = get_fs_from_name("gcs-dataset1")  # You can pass additional kwargs to the function
...
```

Creating an async instance of the gcsfs client:

```python
from polyaxon.fs import get_fs_from_name

...
fs = get_fs_from_name("gcs-dataset1",
                      asynchronous=True)  # You can pass additional kwargs to the function
...
```
