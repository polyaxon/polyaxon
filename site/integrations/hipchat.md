---
title: "Hipchat"
meta_title: "Hipchat"
meta_description: "How to get direct notification from the Polyaxon to your Hipchat channels. Notify Hipchat when an experiment, job, build is finished so that your team stays in sync."
custom_excerpt: "HipChat is a web service for internal private online chat and instant messaging."
image: "../../content/images/integrations/hipchat.png"
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

Notify Hipchat when an experiment, a job, or a build is finished so that your team stays in sync.

## Visit Hipchat to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [Hipchat](https://www.hipchat.com/docs/apiv2/method/create_webhook?_ga=2.203509264.1443225380.1545584678-263232814.1545584678) configuration.
An incoming webhook is a method for Hipchat to receive incoming messages to be posted to your Hipchat team from external services.

## Configure your webhook

Create a secret or a config map with your Hipchat webhook:

```yaml
kubectl create secret generic  notification-secret --from-file=POLYAXON_INTEGRATIONS_WEBHOOKS_HIPCHAT=notification-secret.json -n polyaxon
```

The content of `notification-secret.json` should contain all the webhooks that you want to notify at the same time:

```json
[
  {
    "url": "https://hipchat.com/v2/room/room_id_or_name/webhook"
  }
]
```

## Add your Hipchat connection to Polyaxon notification connections

Now you can add your Hipchat's webhook to the integrations' section:

```yaml
connections:
  - name: hipchat-connection1
    kind: hipchat
    secret:
      name: notification-secret
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to Hipchat using Zapier.
