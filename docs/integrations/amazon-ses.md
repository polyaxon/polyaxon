---
title: "Amazon SES"
meta_description: "How to receive notifications from Polyaxon directly to your email using Amazon SES."
custom_excerpt: "Get email notifications when an experiment, job, build is finished using Amazon SES so everyone that your team stays in sync."
image: "../../content/images/integrations/amazon-ses.png"
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

## Amazon SES

[Amazon SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-smtp.html) is one of the easiest ways to get an outgoing email working reliably. 

## Add your Email notification using Amazon SES to Polyaxon deployment config

Now you can set the email section using your Amazon SES's information:

```yaml
email:
  host: 
  port: 587
  useTls: true
  hostUser: 
  hostPassword: 
```
