---
title: "Slack"
meta_title: "Slack"
meta_description: "How to create custom API and webhook based integrations for the Polyaxon. Notify Slack when an experiment, job, build is finished so everyone that your team stays in sync."
custom_excerpt: "Slack is a collaboration hub for work, no matter what work you do. It's a place where conversations happen, decisions are made, and information is always at your fingertips. With Slack, your team is better connected."
image: "../../content/images/integrations/slack.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - notification
featured: true
visibility: public
status: published
---

## Create a new incoming webhook in Slack

First, you'll need to set up a new incoming webhook in your team's Slack configuration. An incoming webhook is a method for Slack to receive incoming messages to be posted to your Slack team from external services.

![slack-integration1](../../content/images/integrations/slack/img1.png)

## Customise webhook & copy URL

Once the webhook is created, you can optionally customise the channel, name, and icon which the webhook uses whenever it posts a new message. Either way, however, you'll need to copy the Webhook URL at the very top.

![slack-integration2](../../content/images/integrations/slack/img2.png)

## Add your Slack webhook to Polyaxon deployment config

Now you can add your slack webhook to the integrations' section:

```yaml
integrations:
  slack:
    - url: https://hooks.slack.com/services/T6QR3FYN7/BC34VRP/7KRWJAtQWOxjxYgee
    - url: https://hooks.slack.com/services/FGDR3FD34/BC34VRP/7KRWDSFSD3xjxYgee
      channel: channel12
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to your Slack team using Zapier.
