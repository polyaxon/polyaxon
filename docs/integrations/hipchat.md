---
title: "Hipchat"
meta_title: "Hipchat"
meta_description: "How to get direct notification from the Polyaxon to your Hipchat channels. Notify Hipchat when an experiment, job, build is finished so everyone that your team stays in sync."
custom_excerpt: "HipChat is a web service for internal private online chat and instant messaging."
image: "../../content/images/integrations/hipchat.png"
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

## Visit Hipchat to create webhook integration

First, you'll need to set up a new incoming webhook in your team's [Hipchat](https://www.hipchat.com/docs/apiv2/method/create_webhook?_ga=2.203509264.1443225380.1545584678-263232814.1545584678) configuration. 
An incoming webhook is a method for Hipchat to receive incoming messages to be posted to your Hipchat team from external services.

## Add your Hipchat webhook to Polyaxon deployment config

Now you can add your hipchat's webhook to the integrations' section:

```yaml
integrations:
  hipchat:
    - url: https://hipchat.com/v2/room/room_id_or_name/webhook
```

## More automation with Zapier

You can also go further and connect other popular Polyaxon integrations to hipchat using Zapier.
