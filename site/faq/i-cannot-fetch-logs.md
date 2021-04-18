---
title: "I was able to see job's logs but I am not able to see them anymore."
meta_title: "I am getting Bad Request when trying to fetch logs using the web UI or using the CLI - FAQ"
meta_description: "Polyaxon provides several ways for storing the logs, the default method uses a local path on the host node."
featured: false
custom_excerpt: "Polyaxon provides several ways for storing the logs, the default method uses a local path on the host node."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - logging
---

Polyaxon provides several ways for storing the [logs](/docs/setup/connections/artifacts/), the default method uses a local path on the host node.
This is option is sufficient if you are trying the platform and don't want to deal with extra configuration steps, however, when using Polyaxon in a production mode,
you should definitely look at the other persistence strategies.

When the user uses a local path to store logs, a couple of things could happen:
 * The host node might be deleted, or replaced, and all logs will be deleted as well.
 * After an upgrade, all your components might be scheduled on a different node.

Polyaxon provides several options to make robust persistence of your logs.
