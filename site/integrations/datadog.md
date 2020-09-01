---
title: "Datadog"
meta_title: "Datadog"
meta_description: "Polyaxon allows users to integrate Datadog for monitoring."
custom_excerpt: "Datadog is a monitoring service for cloud-scale applications, providing monitoring of servers, databases, tools, and services, through a SaaS-based data analytics platform."
image: "../../content/images/integrations/datadog.png"
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

This guide will help you set up to a [Datadog](https://www.datadoghq.com/) backend to sends these metrics.

## Make sure the default Helm metrics deployment is disabled

```yaml
metrics:
  enabled: false
```

## Set the external service

Send Polyaxon metrics emitted to the Datadog REST API over HTTPS.

```yaml
externalServices:
  metrics:
    enabled: true
    backend: datadog
    options:
      api_key:
      app_key:
      tags: {}
```


## Using the DogStatsD Backend

Use the DogStatsD backend requires a [Datadog Agent](https://docs.datadoghq.com/agent/) to be running with the DogStatsD backend.

```yaml
externalServices:
  metrics:
    enabled: true
    backend: datadog-statsd
    options:
      statsd_host:
      statsd_port: 8125,
      tags: {}
```

