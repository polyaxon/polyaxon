---
title: "I’m getting requests failing on the API from inside experiments/jobs (Authentication credentials were not provided.)"
meta_title: "I’m getting requests failing on the API from inside experiments/jobs (Authentication credentials were not provided.) - FAQ"
meta_description: "Polyaxon uses an ephemeral token to authenticate the jobs/experiments before granting client access to other APIs related to the experiment/job."
featured: false
custom_excerpt: "Polyaxon uses an ephemeral token to authenticate the jobs/experiments before granting client access to other APIs related to the experiment/job."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - api
---

Polyaxon uses an ephemeral token to authenticate the jobs/experiments before granting client access to other APIs related to the experiment/job,
these ephemeral tokens have a TTL with a default value (e.g. 3 hours) after which the token gets invalidated, which in turn makes the job/experiment unable to authenticate.

## Use experiment groups to control the concurrency

You can use experiment groups to only schedule some experiments that you know will have enough resources on your cluster to schedule them and run them.

## Increase the ephemeral token TTL

In case you want to schedule a large number on Kubernetes and you want to avoid this issue, you might want to increase the ephemeral tokens TTL to a larger number,
the value is in seconds:

```yaml
ttl:
  ephemeralToken:  # in seconds, e.g. 3600
```
