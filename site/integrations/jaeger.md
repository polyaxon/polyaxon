---
title: "Jaeger"
meta_title: "Jaeger"
meta_description: "Polyaxon allows users to use Jaeger Open Tracing to trace your API calls in Polyaxon."
custom_excerpt: "Jaeger is an open-source, end-to-end distributed tracing."
image: "../../content/images/integrations/jaeger.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - monitoring
  - setup
featured: false
popularity: 0
visibility: public
status: EE
---

Polyaxon provides an abstraction called `metrics` which is used for internal monitoring, generally timings and various counters.
The default backend `noop` simply discards them.

To enable tracing for Polyaxon EE Control Plane, you can use Jaeger, which is a popular choice for request tracing.

## Make sure the default Helm metrics deployment is disabled

```yaml
metrics:
  enabled: false
```

## Set the external service

```yaml
externalServices:
  metrics:
    enabled: true
    backend: jaeger
    options:
```
