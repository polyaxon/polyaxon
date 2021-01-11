---
title: "PagerDuty"
meta_title: "PagerDuty"
meta_description: "How to get direct notification from the Polyaxon to your PagerDuty channels. Notify PagerDuty when an experiment, job, build is finished so that your team stays in sync."
custom_excerpt: "PagerDuty empowers developers, DevOps, IT operations and business leaders to prevent and resolve business-impacting incidents for exceptional customer experience."
image: "../../content/images/integrations/pagerduty.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - notifications
featured: false
popularity: 0
visibility: public
status: published
---

Notify PagerDuty when an experiment, a job, or a build fails so that your team stays in sync.

## Visit PagerDuty to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [PagerDuty](https://support.pagerduty.com/docs/webhooks) configuration.
An incoming webhook is a method for PagerDuty to receive incoming messages to be posted to your PagerDuty team from external services.

## Configure your webhook

Create a secret or a config map with your PagerDuty webhook:

```yaml
kubectl create secret generic  notification-secret --from-file=POLYAXON_INTEGRATIONS_WEBHOOKS_PAGE_DUTY=notification-secret.json -n polyaxon
```

The content of `notification-secret.json` should contain all the webhooks that you want to notify at the same time:

```json
[
  {
    "url": "url1"
  }
]
```

## Add your PagerDuty connection to Polyaxon notification connections

Now you can add your PagerDuty's webhook to the integrations' section:

```yaml
connections:
  - name: pagerduty-connection1
    kind: pagerduty
    secret:
      name: notification-secret
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to PagerDuty using Zapier.
