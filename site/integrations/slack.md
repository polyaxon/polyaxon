---
title: "Slack"
meta_title: "Slack"
meta_description: "How to create custom API and webhook based integrations for the Polyaxon. Notify Slack when an experiment, job, build is finished so that your team stays in sync."
custom_excerpt: "Slack is a collaboration hub for work, no matter what work you do. It's a place where conversations happen, decisions are made, and information is always at your fingertips. With Slack, your team is better connected."
image: "../../content/images/integrations/slack.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - notifications
featured: true
popularity: 2
visibility: public
status: published
---

Notify Slack when an experiment, a job, or a build is finished so that your team stays in sync.

## Create a new incoming webhook in Slack

First, you'll need to set up a new incoming webhook in your team's Slack configuration. An incoming webhook is a method for Slack to receive incoming messages to be posted to your Slack team from external services.

![slack-integration1](../../content/images/integrations/slack/img1.png)

## Customise webhook & copy URL

Once the webhook is created, you can optionally customize the channel, name, and icon which the webhook uses whenever it posts a new message. Either way, however, you'll need to copy the Webhook URL at the very top.

![slack-integration2](../../content/images/integrations/slack/img2.png)

## Configure your webhook

Create a secret or a config map with your Slack webhook:

```yaml
kubectl create secret generic  notification-secret --from-file=POLYAXON_INTEGRATIONS_WEBHOOKS_PAGE_DUTY=notification-secret.json -n polyaxon
```

The content of `notification-secret.json` should contain all the webhooks that you want to notify at the same time:

```json
[
  {
    "url": "https://hooks.slack.com/services/T6QR3FYN7/BC34VRP/7KRWJAtQWOxjxYgee"
  }
]
```

## Add your Slack connection to Polyaxon notification connections

Now you can add your Slack's webhook to the integrations' section:

```yaml
connections:
  - name: slack-connection1
    kind: slack
    secret:
      name: notification-secret
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to Slack using Zapier.
