---
title: "SendGrid"
meta_title: "SendGrid"
meta_description: "How to receive notifications from Polyaxon directly to your email using sendgrid. Get email notifications when an experiment, job, build is finished using sendgrid so everyone that your team stays in sync."
custom_excerpt: "SendGrid is a cloud-based SMTP provider that acts as an email delivery engine, allowing you to send email without the cost and complexity of maintaining your own email servers."
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
featured: false
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
