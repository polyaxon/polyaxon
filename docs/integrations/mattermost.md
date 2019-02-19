---
title: "Mattermost"
meta_title: "Mattermost"
meta_description: "How to get direct notification from the Polyaxon to your Mattermost channels. Notify Mattermost when an experiment, job, build is finished so everyone that your team stays in sync."
custom_excerpt: "Mattermost is a open-source, self-hostable chat service. It is designed as an internal chat for organisations and companies, and mostly markets itself as an alternative to Slack."
image: "../../content/images/integrations/mattermost.png"
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

## Visit Mattermost to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [Mattermost](https://docs.mattermost.com/developer/webhooks-incoming.html) configuration. 
An incoming webhook is a method for Mattermost to receive incoming messages to be posted to your Mattermost team from external services.

## Add your Mattermost webhook to Polyaxon deployment config

Now you can add your Mattermost's webhook to the integrations' section:

```yaml
integrations:
  mattermost:
    - url: url1
    - url: url2
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to Mattermost using Zapier.
