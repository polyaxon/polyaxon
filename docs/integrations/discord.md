---
title: "Discord"
meta_title: "Discord"
meta_description: "How to get direct notification from the Polyaxon to your Discord channels. Notify Discord when an experiment, job, build is finished so everyone that your team stays in sync."
custom_excerpt: "Discord is a free voice and text communication service like skype."
image: "../../content/images/integrations/discord.png"
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

## Visit Discord to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [Discord](https://discordapp.com/developers/docs/resources/webhook) configuration. 
An incoming webhook is a method for Discord to receive incoming messages to be posted to your Discord team from external services.

## Add your Discord webhook to Polyaxon deployment config

Now you can add your Discord's webhook to the integrations' section:

```yaml
integrations:
  discord:
    - url: url1
    - url: url2
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to discord using Zapier.
