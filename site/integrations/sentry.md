---
title: "Sentry"
meta_title: "Sentry"
meta_description: "Polyaxon allows users to integrate Sentry to monitor your cluster."
custom_excerpt: "Sentry is an open-source error tracking that helps developers monitor and fix crashes in real-time. Iterate continuously. Boost workflow efficiency. Improve user experience."
image: "../../content/images/integrations/sentry.png"
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

Polyaxon EE comes with an opt-in [Sentry](https://sentry.io) integration and provides a key for all customers to report crashes and fix issues very fast.

This integration is disabled by default, and it's not required for the system to function correctly.

If you wish to use your own [Sentry](https://sentry.io) key and not use Polyaxon's key, you can integrate your deployment
of Polyaxon Control Plane and Polyaxon Agents with [Sentry](https://sentry.io),
to get actionable errors and crashes information without leaking any sensitive information, and you can report the issue or open a support ticket.

## Enable Default

The integration is disabled by default, to use the enable the integration:

```yaml
externalServices:
  errors:
    default: true
    backend: sentry
```

## To use your own key, start by creating a Sentry account

[Sentry](https://sentry.io) makes it easy to set up one or more keys.

## Add your Key to your Polyaxon Control Plane deployment

```yaml
externalServices:
  errors:
    enabled: true
    backend: sentry
    options: {platform_dsn: key, cli_dsn: key}
```
