---
title: "New Relic"
meta_title: "New Relic"
meta_description: "Polyaxon allows users to integrate New Relic for monitoring."
custom_excerpt: "New Relic is an observability platform built to help engineers create more perfect software. From monoliths to serverless, you can instrument everything, then analyze, troubleshoot, and optimize your entire software stack. All from one place."
image: "../../content/images/integrations/newrelic.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
  - monitoring
featured: false
popularity: 0
visibility: public
status: EE
---

Polyaxon provides an abstraction called `metrics` which is used for internal monitoring, generally timings and various counters.
The default backend `noop` simply discards them.

This guide will help you set up to a [New Relic](https://www.newrelic.com/) backend to sends these metrics.

## Make sure the default Helm metrics deployment is disabled

```yaml
metrics:
  enabled: false
```

## Set the external service

Add instrumentation and send Polyaxon metrics to New Relic.

```yaml
externalServices:
  metrics:
    enabled: true
    backend: newrelic
    options:
      license_key:
      app_name:
```
