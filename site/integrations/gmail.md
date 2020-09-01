---
title: "Gmail"
meta_title: "Gmail"
meta_description: "How to receive notifications from Polyaxon directly to your email using Gmail. Get email notifications when an experiment, job, build is finished using gmail so everyone in your team stays in sync."
custom_excerpt: "Gmail is email that's intuitive, efficient, and useful. 15 GB of storage, less spam, and mobile access."
image: "../../content/images/integrations/gmail.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - notifications
  - email
featured: false
popularity: 0
visibility: public
status: published
---

Get email notifications when an experiment, a job, or a build is finished using Gmail so that your team stays in sync.

> For production deployments with recommend using other outgoing email services

## Create a Gmail to use for sending emails to your team members

In order to use [Gmail](https://gmail.com) to receive email notifications from Polyaxon,
you should create an account in Gmail.

## Add your Email notification using GMail to Polyaxon deployment config

Now you can set the email section using your Gmail's information:

```yaml
email:
  host: "smtp.gmail.com"
  port: 587
  useTls: true
  hostUser: "foobar@gmail.com"
  hostPassword: "123456"
```
