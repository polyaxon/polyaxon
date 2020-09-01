---
title: "Mailgun"
meta_title: "Mailgun"
meta_description: "How to receive notifications from Polyaxon directly to your email using mailgun. Get email notifications when an experiment, job, build is finished using mailgun so that your team stays in sync."
custom_excerpt: "Mailgun is powerful transactional email APIs that enable you to send, receive, and track emails, built with developers in mind."
image: "../../content/images/integrations/mailgun.png"
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

Get email notifications when an experiment, a job, or a build is finished using mailgun so that your team stays in sync.

## Start by creating a mailgun account

[mailgun](https://www.mailgun.com/sending-email) makes it easy to set up an outgoing email. It has a generous free tier that we recommend you checking out.

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
