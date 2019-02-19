---
title: "PagerDuty"
meta_title: "PagerDuty"
meta_description: "How to get direct notification from the Polyaxon to your PagerDuty channels. Notify PagerDuty when an experiment, job, build is finished so everyone that your team stays in sync."
custom_excerpt: "PagerDuty empowers developers, DevOps, IT operations and business leaders to prevent and resolve business-impacting incidents for exceptional customer experience."
image: "../../content/images/integrations/pagerduty.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - notification
featured: false
visibility: public
status: published
---

## Visit PagerDuty to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [PagerDuty](https://support.pagerduty.com/docs/webhooks) configuration. 
An incoming webhook is a method for PagerDuty to receive incoming messages to be posted to your PagerDuty team from external services.

## Add your PagerDuty webhook to Polyaxon deployment config

Now you can add your PagerDuty's webhook to the integrations' section:

```yaml
integrations:
  pagerduty:
    - url: url1
    - url: url2
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to Pagerduty using Zapier.
