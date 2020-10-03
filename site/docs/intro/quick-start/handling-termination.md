---
title: "Quick Start: Handling Termination"
sub_link: "quick-start/handling-termination"
meta_title: "Handling Termination - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Handling Termination - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - quick-start
sidebar: "intro"
---

Now that we learned how to submit operations, it's important to ensure that ours jobs and services are robust 
using the [termination section](docs/core/specification/termination/).

You can set a default termination on the component level and override the values for each operation, 
or you can only define termination on some operation without setting too much information on the component.
You can also use the [scheduling presets](/docs/core/scheduling-strategies/presets/)
to define one or multiple termination configurations that you can use with one or several of your operations.

## Handling failures with max retries

In order to make your operations resilient to failure that could happen for a variety of reasons:
 * pod preemption, node failure, ...
 * HTTP requests failing when fetching data or assets
 * Service or external API down or unavailable for a short period of time

Polyaxon provides a concept called [max_retries](/docs/core/specification/termination/#maxretries).


## Enforcing SLAs with timeout

It's also important to enforce SLAs (Service Level Agreements) for your operations.
Polyaxon provides the [timeout](/docs/core/specification/termination/#maxretries) section that 
will stop a job or service if it does not succeed or terminate on its own during the time window defined in the termination timeout.

Timeout can be combined with hooks/notifications to deliver the necessary information to users or external services. 


## Debugging with TTL

The third key in the termination section is [ttl](/docs/core/specification/termination/#ttl).
By default, Polyaxon cleans out adn removes all cluster resources as soon as an operation is done.
It is often necessary to keep a job or a service after it's done for sanity checks or debugging purposes. 
