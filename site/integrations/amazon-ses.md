---
title: "Amazon SES"
meta_title: "Amazon SES"
meta_description: "How to receive notifications from Polyaxon directly to your email using Amazon SES. Get email notifications when an experiment, job, build is finished using Amazon SES so everyone in your team stays in sync."
custom_excerpt: "Amazon Simple Email Service (Amazon SES) is a cloud-based email sending service designed to help digital marketers and application developers send marketing, notification, and transactional emails. It is a reliable, cost-effective service for businesses of all sizes that use email to keep in contact with their customers."
image: "../../content/images/integrations/amazon-ses.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - notifications
  - email
  - aws
featured: false
popularity: 0
visibility: public
status: published
---

Integrate Polyaxon with Amazon SES to receive email notifications.

## Setup Amazon SES

[Amazon SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-smtp.html) is one of the easiest ways to get an outgoing email working reliably.

## Add your Email notification using Amazon SES to Polyaxon deployment config

Now you can set the email section using your Amazon SES's SMTP information:

```yaml
email:
  host: 'email-smtp.us-west-1.amazonaws.com'  # Set correct region
  port: 587
  useTls: true
  hostUser:
  hostPassword:
```
