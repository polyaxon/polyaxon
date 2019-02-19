---
title: "Mailgun"
meta_title: "Mailgun"
meta_description: "How to receive notifications from Polyaxon directly to your email using mailgun. Get email notifications when an experiment, job, build is finished using mailgun so everyone that your team stays in sync."
custom_excerpt: "Mailgun is powerful transactional email APIs that enable you to send, receive, and track emails, built with developers in mind."
image: "../../content/images/integrations/mailgun.png"
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

## Start by creating a mailgun account

[mailgun](https://www.mailgun.com/sending-email) makes it easy to setup an outgoing email. It has a generous free tier that we recommend you checking out.

## Add your Email notification using mailgun to Polyaxon deployment config

Now you can set the email setction using your mailgun's information:

```yaml
email:
  host: "smtp.mailgun.org"
  port: 587
  useTls: true
  hostUser: "foobar_mailgun"
  hostPassword: "123456"
```
