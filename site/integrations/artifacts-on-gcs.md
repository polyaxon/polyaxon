---
title: "Artifacts on GCS"
meta_title: "Google GCS"
meta_description: "Using Google Cloud Storage GCS buckets to organize your jobs' outputs and experiments' artifacts. Polyaxon allows users to connect to one or multiple buckets on Google Cloud Storage GCS to store job outputs and experiment artifacts."
custom_excerpt: "Google Cloud Storage is a RESTful online file storage web service for storing and accessing data on Google Cloud Platform infrastructure. The service combines the performance and scalability of Google's cloud with advanced security and sharing capabilities."
image: "../../content/images/integrations/gcs.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - artifacts
  - storage
  - gcp
featured: false
popularity: 2
visibility: public
status: published
---

You can use one or multiple buckets on Google Cloud Storage (GCS) to store logs, job outputs, and experiment artifacts.

## Create a Google cloud storage bucket

You should create a google cloud storage bucket (e.g. plx-artifacts), and you have to assign permission to the bucket.

Google cloud storage provides an easy way to download the access key as a JSON file. You should create a secret based on that JSON file.

## Create a secret on Kubernetes

You can create a secret with an env var of the content of the gcs-key.json:

 * `GC_KEYFILE_DICT` or `GOOGLE_KEYFILE_DICT`

Or you can create a secret to be mounted as a volume:

 * `kubectl create secret generic gcs-secret --from-file=gc-secret.json=path/to/gcs-key.json -n polyaxon`


## Use the secret name and secret key in your data persistence definition

You can use the default mount path `/plx-context/.gc`, Polyaxon will set the `GC_KEY_PATH` to `/plx-context/.gc/gc-secret.json` so the secret must contain --from-file=`gc-secret.json=`

```yaml
artifactsStore:
  name: gcs-artifacts
  kind: gcs
  schema:
    bucket: "gs://gcs-artifacts"
  secret:
    name: "gcs-secret"
    mountPath: /plx-context/.gc
```

You can also use a different mount path, e.g. `/etc/gcs/gc-secret.json`, in which case you need to provide an env var to tell the SDK where to look for the secret:

```bash
kubectl create configmap gc-key-path --from-literal GC_KEY_PATH="/etc/gcs/gc-secret.json" -n polyaxon
```

```yaml
artifactsStore:
  name: gcs-artifacts
  kind: gcs
  schema:
    bucket: "gs://gcs-datasets"
  secret:
    name: "gc-secret"
    mountPath: /etc/gcs
  configMap:
    name: gc-key-path
```

## Update/Install Polyaxon deployment

You can [deploy/upgrade](/docs/setup/) your Polyaxon CE or Polyaxon Agent deployment with access to the artifacts store.
