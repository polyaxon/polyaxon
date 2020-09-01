---
title: "Statsd"
meta_title: "Statsd"
meta_description: "Polyaxon allows users to integrate statsd for monitoring."
custom_excerpt: "Statsd is daemon for easy but powerful stats aggregation."
image: "../../content/images/integrations/statsd.png"
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

Polyaxon provides an abstraction called ‘metrics’ which is used for internal monitoring, generally timings and various counters.
The default backend `noop` simply discards them.

This guide will help you set up a statsd backend to sends these metrics.

## Using the default Helm metrics deployment

Polyaxon provides a built-in statsd exporter in the Helm chart that can be enabled, the backend will be configured automatically.

```yaml
metrics:
  enabled: true
```

## Using a custom backend

```yaml
externalServices:
  metrics:
    enabled: true
    backend: statsd
    options: {host: host, port: 8125}
```
