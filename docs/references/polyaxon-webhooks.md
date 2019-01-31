---
title: "Polyaxon Webhooks"
sub_link: "polyaxon-webhooks"
meta_title: "Polyaxon Webhooks - Polyaxon References"
meta_description: "Polyaxon WebhooksWebhooks are specific events triggered when something happens in Polyaxon, like experiment success, job deletion, ..."
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
The only required fields to setup a new webhook are a trigger event and target URL to notify. 
This target URL is your application URL, 
the endpoint where the POST request will be sent. 
Of course, this URL must be reachable from the Internet.

If the server responds with 2xx HTTP response, 
the delivery is considered successful. 
Anything else is considered a failure of some kind, 
and anything returned in the body of the response will be discarded.


## Available events

Currently Polyaxon has support a couple of events on which webhook can be setup, 
but we are working on adding more:

|Event|Description|
|-----|-----------|
|`experiments.done`|Triggered whenever an experiment reached a done status|
|`experiments.succeeded`|Triggered whenever an experiment succeeds|
|`experiments.failed`|Triggered whenever an experiment fails|
|`experiments.stopped`|Triggered whenever an experiment is stopped|
|`groups.done`|Triggered whenever an experiment group reached a done status|
|`groups.failed`|Triggered whenever an experiment group fails|
|`groups.stopped`|Triggered whenever an experiment group is stopped|
|`jobs.done`|Triggered whenever an job reached a done status|
|`jobs.succeeded`|Triggered whenever an job succeeds|
|`jobs.failed`|Triggered whenever an job fails|
|`jobs.stopped`|Triggered whenever an job is stopped|
|`builds.done`|Triggered whenever an build reached a done status|
|`builds.succeeded`|Triggered whenever an build succeeds|
|`builds.failed`|Triggered whenever an build fails|
|`builds.stopped`|Triggered whenever an build is stopped|
