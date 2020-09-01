---
title: "SendGrid"
meta_title: "SendGrid"
meta_description: "How to receive notifications from Polyaxon directly to your email using Sendgrid. Get email notifications when an experiment, job, build is finished using Sendgrid so that your team stays in sync."
custom_excerpt: "SendGrid is a cloud-based SMTP provider that acts as an email delivery engine, allowing you to send email without the cost and complexity of maintaining your own email servers."
image: "../../content/images/integrations/sendgrid.jpg"
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

Get email notifications when an experiment, a job, or a build is finished using Sendgrid so that your team stays in sync.

## Start by creating a Sendgrid account

[Sendgrid](https://sendgrid.com/solutions/smtp-service/) makes it easy to set up an smtp email service.

## Add your Email notification using Sendgrid to Polyaxon deployment config

Now you can set the email section using your Sendgrid's information:

```yaml
email:
  host: "smtp.sendgrid.net"
  port: 587
  useTls: true
  hostUser: "sendgrid_username"
  hostPassword: "123456"
```
