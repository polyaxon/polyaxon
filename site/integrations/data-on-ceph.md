---
title: "Data on Ceph"
meta_title: "Ceph"
meta_description: "Using data on Ceph in your Polyaxon experiments and jobs. Polyaxon allows users to connect to one or multiple buckets on Ceph to access data directly on your machine learning experiments."
custom_excerpt: "Ceph is an open-source software-defined storage platform that implements object storage on a single distributed computer cluster and provides 3-in-1 interfaces for object-, block- and file-level storage. Ceph aims primarily for completely distributed operation without a single point of failure, scalability to the exabyte level, and to be freely available. Since version 12 Ceph does not rely on other filesystems and can directly manage HDDs and SSDs with its own storage backend BlueStore and can completely self reliantly expose a POSIX filesystem."
image: "../../content/images/integrations/ceph.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - data-stores
  - storage
featured: false
popularity: 0
visibility: public
status: published
---

You can use one or multiple buckets on Ceph to access data directly on your machine learning experiments and jobs.

## Deploy Ceph

Before using Ceph, you need to deploy it and create a bucket (or several) to host your data.

## Create a bucket on Ceph

You should create a bucket (e.g. plx-storage) where you will host your data.

## Use the bucket in Polyaxon

In order to use the buckets with Polyaxon, you can follow the [S3 DataStore integration](/integrations/data-on-s3/).

Please note that you will need to set as well `AWS_ENDPOINT_URL` or `S3_ENDPOINT_URL`.
