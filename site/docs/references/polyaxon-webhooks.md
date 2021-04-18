---
title: "Polyaxon Webhooks"
sub_link: "polyaxon-webhooks"
meta_title: "Polyaxon Webhooks - Polyaxon References"
meta_description: "Polyaxon Webhooks are specific events triggered when something happens in Polyaxon, like experiment success, job deletion, ..."
visibility: public
status: published
tags:
  - webhooks
  - reference
  - polyaxon
  - integration
---

Webhooks are specific events triggered when something happens in Polyaxon,
like experiment success, job deletion, ...


## Overview

Webhooks allows Polyaxon to send POST requests to user-configured URLs in order to send them a notification about it.
The request body is a JSON object containing data about the triggered event,
and the end result could be something as simple as a Slack notification
or as complex as a triggering a pipeline on a different infrastructure.


## Setting up a webhook

Configuring webhooks can be done through the deployment config file.
The only required fields to set up a new webhook are a trigger event and a target URL to notify.
This target URL is your application URL,
the endpoint where the POST request will be sent.
Of course, this URL must be reachable from the Internet.

If the server responds with 2xx HTTP response,
the delivery is considered successful.
Anything else is considered a failure of some kind,
and anything returned in the body of the response will be discarded.


## Available events

Currently Polyaxon supports a couple of events on which webhook can be setup,
but we are working on adding more:

|Event|Description|
|-----|-----------|
|`done`|Triggered whenever a run reached a done status|
|`succeeded`|Triggered whenever a run experiment succeeds|
|`failed`|Triggered whenever a run experiment fails|
|`stopped`|Triggered whenever a run experiment is stopped|
