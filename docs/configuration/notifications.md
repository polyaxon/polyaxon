---
title: "Notifications"
sub_link: "notifications"
meta_title: "Notifications and events in Polyaxon - Configuration"
meta_description: "You can configure Polyaxon to send notifications to users about event changes in the platform."
tags:
    - configuration
    - polyaxon
    - notifications
    - events
    - hooks
sidebar: "configuration"
---

You can configure Polyaxon to send notifications to users about event changes in the platform.

## Email

In order to send notification via email, the platform needs to identify an outgoing email (SMTP) account
where you can have Polyaxon send mail. There are some free outgoing email services like: Mailgun, SendGrid, or for AWS users Amazon SES.
These services are designed to send email from servers, and are by far the easiest way to get outgoing email working reliably.

### Email configuration

It's easy to configure outgoing emails in Polyaxon, you need to fill the email section in your config file:

```yaml
email:
  host:
  port:
  useTls: false
  hostUser:
  hostPassword:
```

#### e.g. Email with Mailgun

```yaml
email:
  host: "smtp.mailgun.org"
  port: 587
  useTls: true
  hostUser: "foobar_mailgun"
  hostPassword: "123456"
```


#### e.g. Email with gmail

```yaml
email:
  host: "smtp.gmail.com"
  port: 587
  useTls: true
  hostUser: "foobar@gmail.com"
  hostPassword: "123456"
```


## Slack

You can get notification directly to your your slack team's channels.
In order to do that you need to link one or multiple slack webhook, 
Please check this [integration guide](/integrations/slack/) for to set Slack notifications.

## HipChat

In order to configure Polyaxon to send notification to HipChat, you need to set the hipchat's integration section. 
Please check this [integration guide](/integrations/hipchat/) for to set HipChat notifications.


## Discord

In order to configure Polyaxon to send notification to Discord, you need to set the discord's integration section. 
Please check this [integration guide](/integrations/discord/) for to set Discord notifications.


## Mattermost

In order to configure Polyaxon to send notification to Mattermost, you need to set the mattermost's integration section. 
Please check this [integration guide](/integrations/mattermost/) for to set Mattermost notifications.


## PagerDuty

In order to configure Polyaxon to send notification to PagerDuty, you need to set the pagerduty's integration section. 
Please check this [integration guide](/integrations/pagerduty/) for to set PagerDuty notifications.


## Webhooks

To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use. 
Please check this [integration guide](/integrations/webhooks/) for to set Webhooks notifications.
