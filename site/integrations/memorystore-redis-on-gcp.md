---
title: "MemoryStore for Redis on GCP"
meta_title: "Cloud MemoryStore for Redis on GCP"
meta_description: "Using Google cloud Platform Cloud MemoryStore for Redis for a high available redis to use with Polyaxon."
custom_excerpt: "Cloud MemoryStore Fully-managed in-memory data store service for Redis"
image: "../../content/images/integrations/memorystore.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
  - redis
featured: false
popularity: 1
visibility: public
status: published
---

This integration is about using [Cloud MemoryStore for Redis](https://cloud.google.com/memorystore/docs/redis/) for Polyaxon.


## Pre-requisites

A valid GCP Subscription.


## Create a Cloud MemoryStore

Create a [MemoryStore instance](https://console.cloud.google.com/memorystore)


## Update polyaxon deployment

Update your config deployment file and upgrade.

```yaml
redis:
  enabled: false

externalServices:
  redis:
    host: "10.0.16.3"
```

