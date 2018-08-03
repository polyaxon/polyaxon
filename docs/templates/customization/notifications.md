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

```
email:
  host: "smtp.mailgun.org"
  port: 587
  useTls: true
  hostUser: "foobar@gmail.com"
  hostPassword: "123456"
```


#### e.g. Email with gmail

```
email:
  host: "smtp.gmail.com"
  port: 587
  useTls: true
  hostUser: "foobar@gmail.com"
  hostPassword: "123456"
```


## Slack

You can get notification directly to your your slack team's channels.
In order to do that you need to link one or multiple slack webhook:

```
integration:
  slack:
    - url: https://hooks.slack.com/services/T6QR3FYN7/BC34VRP/7KRWJAtQWOxjxYgee
    - url: https://hooks.slack.com/services/FGDR3FD34/BC34VRP/7KRWDSFSD3xjxYgee
      channel: channel12
```


## HipChat

In order to configure Polyaxon to send notification to HipChat, you need to set the hipchat's integration section:

```
integration:
  hipchat:
    - url: https://hipchat.com/v2/room/room_id_or_name/webhook
```


## Discord

In order to configure Polyaxon to send notification to Discord, you need to set the discord's integration section:

```
integration:
  discord:
    - url: url1
    - url: url2
```


## Mattermost

In order to configure Polyaxon to send notification to Mattermost, you need to set the mattermost's integration section:

```
integration:
  mattermost:
    - url: url1
```

## PagerDuty

In order to configure Polyaxon to send notification to PagerDuty, you need to set the pagerduty's integration section:

```
integration:
  pagerduty:
    - url: url1
```


## Webhooks

To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use:

```
integration:
  webhook:
    - url: url1
    - url: url2
      method: post
    - url: url2
      method: get
```
