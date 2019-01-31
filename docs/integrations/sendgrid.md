---
title: "sendgrid"
meta_description: "How to receive notifications from Polyaxon directly to your email using sendgrid."
custom_excerpt: "Get email notifications when an experiment, job, build is finished using sendgrid so everyone that your team stays in sync."
image: "../../content/images/integrations/sendgrid.jpg"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - notification
  - email
featured: true
visibility: public
status: published
---

## Start by creating a sendgrid account

[sendgrid](https://sendgrid.com/solutions/smtp-service/) makes it easy to setup an smtp email service.

## Add your Email notification using sendgrid to Polyaxon deployment config

Now you can set the email section using your sendgrid's information:

```yaml
email:
  host: "smtp.sendgrid.net"
  port: 587
  useTls: true
  hostUser: "sendgrid_username"
  hostPassword: "123456"
```
