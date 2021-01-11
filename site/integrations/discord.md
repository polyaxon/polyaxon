---
title: "Discord"
meta_title: "Discord"
meta_description: "How to get direct notification from the Polyaxon to your Discord channels. Notify Discord when an experiment, job, build is finished so that your team stays in sync."
custom_excerpt: "Discord is a free voice and text communication service like skype."
image: "../../content/images/integrations/discord.png"
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

Notify Discord when an experiment, a job, or a build is finished so that your team stays in sync.

## Visit Discord to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [Discord](https://discordapp.com/developers/docs/resources/webhook) configuration.
An incoming webhook is a method for Discord to receive incoming messages to be posted to your Discord team from external services.

## Configure your webhook

Create a secret or a config map with your Discord webhook:

```yaml
kubectl create secret generic  notification-secret --from-file=POLYAXON_INTEGRATIONS_WEBHOOKS_DISCORD=notification-secret.json -n polyaxon
```

The content of `notification-secret.json` should contain all the webhooks that you want to notify at the same time:

```json
[
  {
    "url": "https://url1.com/services/FFFF$$$$$/FFFF$$$$$/FFFF$$$$$sktkeXUWiaifxIFFFF$$$$$"
  }
]
```

## Add your Discord connection to Polyaxon notification connections

Now you can add your Discord's webhook to the integrations' section:

```yaml
connections:
  - name: discord-connection1
    kind: discord
    secret:
      name: notification-secret
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to Discord using Zapier.
