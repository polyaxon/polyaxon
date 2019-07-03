---
title: "Cloud MemoryStore for Redis on GCP"
meta_title: "Cloud MemoryStore for Redis on GCP"
meta_description: "Using Google cloud Platform Cloud MemoryStore for Redis for a high available redis to use with Polyaxon."
custom_excerpt: "CLOUD MEMORYSTORE Fully-managed in-memory data store service for Redis"
image: "../../content/images/integrations/memorystore.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - database
featured: false
visibility: public
status: published
---

This integration is about using [Cloud MemoryStore for Redis](https://cloud.google.com/memorystore/docs/redis/) for Polyaxon.

> You can use this integration can used with all Polyaxon deployment types


## Pre-requisites

A valid GCP Subscription.


## Create an Cloud MemoryStore

Create a [MemoryStore instance](https://console.cloud.google.com/memorystore)


### Update polyaxon deployment

```yaml
redis:
  enabled: false
  
externalServices:
  redis:
    host: "10.0.16.3"
``` 

